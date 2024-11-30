import psycopg2
import logging
import os
from openai import OpenAI


def find_k_nearest(vector: list[float], k: int, lang_to_exclue: str|None = None) -> list[list[str, float]]:
    """
    Function to find K closest vectors in the database given a vector

    vector: list[float]
    k: int

    """

    if len(vector) != 1536:
        raise ValueError("Vector size error")

    # database connection
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("PGDATABASE"),
            user=os.getenv("PGUSER"),
            password=os.getenv("PGPASSWORD"),
            host=os.getenv("PGHOST"),
            port=os.getenv("PGPORT", 5432),
        )

        cursor = conn.cursor()
        logging.debug("Database connected")
    except psycopg2.Error as e:
        logging.error(f"Error connecting to the database \n{e}\n")

    if lang_to_exclue:
        where_stantment = f"WHERE doc_langauge != %s"
        query_params = [str(vector), lang_to_exclue, str(k)]
    else:
        where_stantment = ""
        query_params = [str(vector), str(k)]

    query = f"""
        SELECT 
            doc_title, 
            doc_langauge AS doc_language,
            sentence, 
            index_in_doc,
            embedding <=> %s as cosine_distance
        FROM embeddings
        {where_stantment}
        ORDER BY cosine_distance
        LIMIT %s 
    """

    cursor.execute(query, query_params)
    rows = cursor.fetchall()

    return rows


if __name__ == "__main__":
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model_name = os.getenv("MODEL_NAME")
    #  
    sent_to_compare = "2015 saw the premiere of ''The Last Jedi'' (2017) and ''The Rise of Skywalker."
    response = openai_client.embeddings.create(input=sent_to_compare, model=model_name)

    vector = response.data[0].embedding

    test = find_k_nearest(vector, 5, "en")
    test2 = find_k_nearest(vector, 5)

    pass
