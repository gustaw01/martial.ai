from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import psycopg2
import os
import logging
from http import HTTPStatus
from fastapi import HTTPException
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv("app/.env")
model_name = os.getenv("MODEL_NAME")
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("PGDATABASE"),
            user=os.getenv("PGUSER"),
            password=os.getenv("PGPASSWORD"),
            host=os.getenv("PGHOST"),
            port=os.getenv("PGPORT", 5432),
        )
        logging.debug("Database connected")
        return conn
    except psycopg2.Error as error:
        logging.error(f"Error connecting to the database \n{error}\nExiting..")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            detail="Database connection error",
        )


def calculate_cosine_similarity(vector1, vector2):
    return cosine_similarity([vector1], [vector2])[0][0]


def blast(
    target_sentences, document_data, threshold=0.8, max_forward=5, max_backward=5
):
    """
    target_sentences: Lista embeddingów zdań, które chcemy porównać (stanowią dokument).
    document_data: Lista zdań z dokumentu bazy danych.
    threshold: Minimalne cosine similarity dla uznania zdania za podobne.
    max_forward: Maksymalna liczba zdań do przodu, które można sprawdzić dla dopasowania w dokumencie z bazy.
    max_backward: Maksymalna liczba zdań do tyłu, które można sprawdzić dla dopasowania w dokumencie z bazy.
    """
    sequences = []
    used_sentence_ids = set()

    for target_index, target_sentence in enumerate(target_sentences):
        target_embedding = np.array(target_sentence)

        for i, record in enumerate(document_data):
            sentence_id = record["id"]
            if sentence_id in used_sentence_ids:
                continue

            embedding = np.array(record["embedding"])
            similarity = calculate_cosine_similarity(target_embedding, embedding)

            if similarity >= threshold:
                sequence = [
                    {
                        "sentence_id": sentence_id,
                        "text": record["sentence"],
                        "index_in_doc": record["index_in_doc"],
                        "similarity": similarity,
                    }
                ]
                used_sentence_ids.add(sentence_id)
                current_index = i

                for next_target_sentence in target_sentences[target_index + 1 :]:
                    next_target_embedding = np.array(next_target_sentence)
                    next_match_found = False

                    for j in range(
                        current_index + 1,
                        min(current_index + 1 + max_forward, len(document_data)),
                    ):
                        next_record = document_data[j]
                        next_sentence_id = next_record["id"]

                        if next_sentence_id in used_sentence_ids:
                            continue

                        next_embedding = np.array(next_record["embedding"])
                        next_similarity = calculate_cosine_similarity(
                            next_target_embedding, next_embedding
                        )

                        if next_similarity >= threshold:
                            sequence.append(
                                {
                                    "sentence_id": next_sentence_id,
                                    "text": next_record["sentence"],
                                    "index_in_doc": next_record["index_in_doc"],
                                    "similarity": next_similarity,
                                }
                            )
                            used_sentence_ids.add(next_sentence_id)
                            current_index = j
                            next_match_found = True
                            break

                    if not next_match_found:
                        break

                for prev_target_sentence in reversed(target_sentences[:target_index]):
                    prev_target_embedding = np.array(prev_target_sentence)
                    previous_match_found = False

                    for j in range(max(0, current_index - max_backward), current_index):
                        prev_record = document_data[j]
                        prev_sentence_id = prev_record["id"]

                        if prev_sentence_id in used_sentence_ids:
                            continue

                        prev_embedding = np.array(prev_record["embedding"])
                        prev_similarity = calculate_cosine_similarity(
                            prev_target_embedding, prev_embedding
                        )

                        if prev_similarity >= threshold:
                            sequence.insert(
                                0,
                                {
                                    "sentence_id": prev_sentence_id,
                                    "text": prev_record["sentence"],
                                    "index_in_doc": prev_record["index_in_doc"],
                                    "similarity": prev_similarity,
                                },
                            )
                            used_sentence_ids.add(prev_sentence_id)
                            current_index = j
                            previous_match_found = True
                            break

                    if not previous_match_found:
                        break

                sequences.append(sequence)

                break

    return sequences


target_sentences = [
    "2015 saw the premiere of ''The Last Jedi'' (2017) and ''The Rise of Skywalker.",
    "W 2015 roku całkowita wartość franczyzy wyniosła 42 mld USD, co pozwoliło zająć jej 2. miejsce wśród najbardziej dochodowych franczyz.",  # 18
    "Akcja filmów i innych kanonicznych elementów franczyzy opisuje ponad 60 lat historii.",  # 21
    "Akcja utworów należących do ''Legend'' sięga nawet ponad 25 000 lat wstecz, oraz wiek naprzód, opisując niekanoniczną przyszłość w której obca rasa zwana Yuuzhan Vong przybywa z innej galaktyki.",  # 22
    "Nie wiem o czym napisać, pozdrawiam.",
]
target_embeddings = []

for sentence in target_sentences:
    response = openai_client.embeddings.create(input=sentence, model=model_name)
    target_embeddings.append(response.data[0].embedding)


conn = get_db_connection()
cursor = conn.cursor()


def get_sentences_from_doc(doc_title):
    query = """
    SELECT id, doc_title, doc_langauge, sentence, index_in_doc, embedding
    FROM embeddings
    WHERE doc_title = %s
    """
    cursor.execute(query, (doc_title,))

    rows = cursor.fetchall()
    results = []
    for row in rows:
        results.append(
            {
                "id": row[0],
                "doc_title": row[1],
                "doc_lang": row[2],
                "sentence": row[3],
                "index_in_doc": row[4],
                "embedding": json.loads(row[5]),
            }
        )
    return results


doc_title = "Gwiezdne wojny"
sentences_from_db = get_sentences_from_doc(doc_title)
sequences = blast(
    target_embeddings, sentences_from_db, threshold=0.89, max_forward=3, max_backward=2
)

print(f"Found {len(sequences)} sequences.")
for seq_index, sequence in enumerate(sequences):
    print(f"Sequence {seq_index + 1}:")
    for sentence in sequence:
        print(
            f"  ID: {sentence['sentence_id']}, Similarity: {sentence['similarity']:.2f}"
        )
        print(f"  Text: {sentence['text']}")
    print()
