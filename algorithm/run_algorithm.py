from algorithm.blast import blast, get_sentences_from_doc
from algorithm.create_embeddings import create_embeddings_multithreading
from algorithm.find_k_nearest import find_k_nearest
from openai import OpenAI
import os
import psycopg2
from collections import Counter


def get_most_common_docs(rows: list, n: int):

    cc = Counter()

    for row in rows:
        cc.update(row[0])

    n_most_common = cc.most_common(n)
    n_most_common_docs, _ = zip(*n_most_common) # pythonic or what

    return  n_most_common_docs



def run_algorithm(text: str, language: str):

    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    conn = psycopg2.connect(
        dbname=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        host=os.getenv("PGHOST"),
        port=os.getenv("PGPORT", 5432),
    )

    model_name = "text-embedding-ada-002" # fix this hard coded name
    text_embeddings = create_embeddings_multithreading(text=text, language=language, model_name=model_name, client=openai_client) 

    # getting plagiarism in the same language
    k_nearest = find_k_nearest(vector=text_embeddings, n_articles=3, conn=conn)
    most_common_docs = get_most_common_docs(k_nearest)

    plagiarisms = []
    for most_common_doc in most_common_docs:
        sentences_from_db = get_sentences_from_doc(most_common_doc)
        plagiarisms.append(blast(text_embeddings, sentences_from_db))

    # plagiarism in another language
    k_nearest_other_langs = find_k_nearest(vector=text_embeddings, n_articles=3, conn=conn, lang_to_exclue=language)
    most_common_docs_other_langs = get_most_common_docs(k_nearest_other_langs)

    plagiarisms_other_lang = []
    for doc_other_lang in most_common_docs_other_langs:
        sentences_from_db_other_lang = get_sentences_from_doc(doc_other_lang)
        plagiarisms_other_lang.append(sentences_from_db_other_lang)


    return (plagiarisms, plagiarisms_other_lang)




