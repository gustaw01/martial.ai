import psycopg2
import logging
import os
from openai import OpenAI


def find_k_nearest(vector: list[float], k: int, table_name: int = "embeddings") -> list[list[str, float]]:
    """
    Function to find K closest vectors in the database given a vector

    vector: list[float]
    k: int

    """

    
    if len(vector) != 1536: 
        raise ValueError("Vector size")


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
        logging.error(f"Error connecting to the database \n{e}\nExiting..")

    query = f"""
        SELECT * FROM {table_name}
        ORDER BY embedding <=> %s
        LIMIT %s 
    """

    cursor.execute(query, [str(vector), str(k)])
    rows = cursor.fetchall()

    return rows 

if __name__ == "__main__":
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model_name = os.getenv("MODEL_NAME")
    #  2015 roku odbyła się premiera filmu ''Ostatni Jedi'' (2017) oraz ''Skywalker.
    sent_to_compare = "I 2015 fandt premieren på filmene 'The Last Jedi' (2017) og 'Rise of Skywalker' sted."
    response = openai_client.embeddings.create(input=sent_to_compare, model=model_name)

    vector = response.data[0].embedding

    test = find_k_nearest(vector, 5, "embeddings_test2")
