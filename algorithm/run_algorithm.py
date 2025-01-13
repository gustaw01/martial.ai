from openai import OpenAI
import os
import psycopg2
from collections import Counter
from functools import partial
from itertools import chain
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../algorithm")))

from blast import blast, get_sentences_from_doc
from create_embeddings import create_embeddings_multithreading
from find_k_nearest import find_k_nearest

def get_most_common_docs(rows: list, n: int = 3):

    cc = Counter([(row[0], row[1]) for row in rows])

    n_most_common = cc.most_common(n)
    n_most_common_docs, _ = zip(*n_most_common) # pythonic or what

    return  n_most_common_docs


def reduce_plagiarisms(plagiarisms: list, split_text: list[str]):

    total_similarity = .0

    reduced_plagiarisms = []
    for i, sentence in enumerate(split_text):
        matches_for_sent = []
        for plag_row in plagiarisms:
            for match in plag_row:
                if match["matched_target_id"] == i:
                    matches_for_sent.append(match)

        if len(matches_for_sent) > 0:
            top_match = sorted(matches_for_sent, key=lambda m: m["similarity"])[-1]
            reduced_plagiarisms.append({
                "matched_sentence": top_match["text"],
                "document_sentence": sentence,
                "similarity": float(top_match["similarity"]),
                "index_in_text": i

            })
            total_similarity += float(top_match["similarity"])
        else:
            reduced_plagiarisms.append({
                "matched_sentence": "",
                "document_sentence": sentence,
                "similarity": .0,
                "index_in_text": i

            })

    score = total_similarity / len(split_text)
    
    return reduced_plagiarisms, score



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
    vec_length = 1536
    text_embeddings, split_text = create_embeddings_multithreading(text=text, language=language, model_name=model_name, client=openai_client) 

    # getting plagiarism in the same language
    # TODO move a bunch of this code to the databse
    find_k_nearest_partial = partial(find_k_nearest, n_articles=3, conn=conn, vec_lenght=vec_length)
    rows = []
    for embedding in text_embeddings:
        rows.extend(find_k_nearest_partial(embedding))
    most_common_docs = get_most_common_docs(rows)

    plagiarisms = []
    for most_common_doc, most_common_lang in most_common_docs:
        sentences_from_db = get_sentences_from_doc(most_common_doc, most_common_lang)
        plagiarisms.extend(blast(text_embeddings, sentences_from_db, threshold=0.92))

    # plagiarism in another language
    find_k_nearest_other_lang_partial = partial(find_k_nearest, n_articles=3, conn=conn, lang_to_exclue=language, vec_lenght=vec_length)

    rows = []
    for embedding in text_embeddings:
        rows.extend(find_k_nearest_other_lang_partial(embedding))

    most_common_docs_other_langs = get_most_common_docs(rows)
    plagiarisms_other_lang = []
    for doc_other_lang, lang_other_lang in most_common_docs_other_langs:
        sentences_from_db_other_lang = get_sentences_from_doc(doc_other_lang, lang_other_lang)
        plagiarisms_other_lang.extend(blast(text_embeddings, sentences_from_db_other_lang, threshold=0.85))

    # Removing the lowest 
    reduced_plagiarisms, score = reduce_plagiarisms(plagiarisms, split_text)
    reduced_plagiarisms_other_lang, score_other_lang = reduce_plagiarisms(plagiarisms_other_lang, split_text)

    ret_dict = {
        "plagiarism": reduced_plagiarisms,
        "plagiarisms_other_lang": reduced_plagiarisms_other_lang,
        "rating": score,
        "rating_other_lang": score_other_lang
    }

    return ret_dict




