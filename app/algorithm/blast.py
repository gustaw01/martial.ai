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
    target_embeddings, document_data, threshold=0.8, max_forward=5, max_backward=5
):
    """
    Args:
        target_embeddings: List of sentence embeddings to compare (constituting a document).
        document_data: List of sentences from the database document.
        threshold: Minimum cosine similarity to consider a sentence as similar.
        max_forward: Maximum number of sentences forward to check for a match in the database document.
        max_backward: Maximum number of sentences backward to check for a match in the database document.

    Returns:
        List of sequences of similar sentences.
        sentence_id: sentence ID in database
        text: text of the sentence from database
        similarity: cosine similarity of target and database sentence
        matched_target_id: index of the target sentence that was matched
    """
    sequences = []
    used_sentence_ids = set()

    for target_index, target_sentence in enumerate(target_embeddings):
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
                        "matched_target_id": target_index,
                    }
                ]
                used_sentence_ids.add(sentence_id)
                current_index = i

                for j in range(
                    current_index + 1,
                    min(current_index + 1 + max_forward, len(document_data)),
                ):
                    next_record = document_data[j]
                    next_sentence_id = next_record["id"]
                    if next_sentence_id in used_sentence_ids:
                        continue

                    next_embedding = np.array(next_record["embedding"])
                    for next_target_sentence_index, next_target_sentence in enumerate(
                        target_embeddings[target_index + 1 :], start=target_index + 1
                    ):
                        next_target_embedding = np.array(next_target_sentence)
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
                                    "matched_target_id": next_target_sentence_index,
                                }
                            )
                            used_sentence_ids.add(next_sentence_id)
                            break

                for j in range(max(0, current_index - max_backward), current_index):
                    prev_record = document_data[j]
                    prev_sentence_id = prev_record["id"]
                    if prev_sentence_id in used_sentence_ids:
                        continue

                    prev_embedding = np.array(prev_record["embedding"])
                    for prev_target_sentence_index, prev_target_sentence in enumerate(
                        reversed(target_embeddings[:target_index]), start=0
                    ):
                        prev_target_embedding = np.array(prev_target_sentence)
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
                                    "matched_target_id": target_index
                                    - prev_target_sentence_index
                                    - 1,
                                },
                            )
                            used_sentence_ids.add(prev_sentence_id)
                            break

                sequences.append(sequence)
                break

    return sequences


def get_sentences_from_doc(doc_title, lang=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    if lang:
        query_cond = f"AND doc_langauge = %s"
        params = (doc_title, lang)
    else:
        query_cond = ""
        params = (doc_title, )

    query = f"""
    SELECT id, doc_title, doc_langauge, sentence, index_in_doc, embedding
    FROM embeddings
    WHERE doc_title = %s {query_cond}
    """
    cursor.execute(query, params)

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
