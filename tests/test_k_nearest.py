
from openai import OpenAI
import psycopg2
import os
import time
import sys
import dotenv
from test_data import TEST_TEXT # importing text from the other file

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
dotenv.load_dotenv()

from app.algorithm.find_k_nearest import find_k_nearest

def test_find_k_nearest():
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model_name = os.getenv("MODEL_NAME")

    conn = psycopg2.connect(
        dbname=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        host=os.getenv("PGHOST"),
        port=os.getenv("PGPORT", 5432),
    )

    vec_lenght = int(os.getenv("VECTOR_LENGTH"))

    # This sentence was translated from Polish into English
    # We are hoping to find the same sentence but in the original language
    translated_sent = "2015 saw the premiere of ''The Last Jedi'' (2017) and ''The Rise of Skywalker."
    org_lang_title = "Gwiezdne wojny"
    org_lang_doc_index = 11
    n_articles = 2

    # embeddings for translated sentece
    response = openai_client.embeddings.create(input=translated_sent, model=model_name)
    vector = response.data[0].embedding

    # calcualating the distance
    start_time = time.time()
    test_output = find_k_nearest(vector, n_articles, conn, vec_lenght, "en")
    print(f"find_k_nearest execution time {time.time() - start_time}s")

    assert len(test_output) == n_articles

    # testing if desired text was found
    assert test_output[0][0] == org_lang_title
    assert test_output[0][3] == org_lang_doc_index

    # check if ignoring the langauge works
    assert all(map(lambda x: x[1] != "en", test_output))