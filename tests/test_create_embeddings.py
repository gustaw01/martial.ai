from openai import OpenAI
import os
import time
import pytest
import sys
import dotenv
from nltk import sent_tokenize
from nltk.langnames import langname
import math
from test_data import TEST_TEXT # importing text from the other file

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../algorithm")))
dotenv.load_dotenv()

from create_embeddings import create_embeddings, create_embeddings_multithreading


def cosine_similarity(v1, v2):
    "compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)"
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]
        y = v2[i]
        sumxx += x * x
        sumyy += y * y
        sumxy += x * y
    return sumxy / math.sqrt(sumxx * sumyy)


@pytest.mark.parametrize(
    "text, language, model_name",
    [
        (TEST_TEXT, "en", os.getenv("MODEL_NAME")),
    ],
)
def test_create_embeddings(text, language, model_name):
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    n_sentences = len(sent_tokenize(text, langname(language).lower()))
    print(f"Testing emebddings on {n_sentences} sentences")

    start_single = time.time()
    single_thread_result = create_embeddings(text, language, model_name, openai_client)
    single_thread_time = time.time() - start_single

    start_multi = time.time()
    multi_thread_result = create_embeddings_multithreading(text, language, model_name, openai_client)
    multi_thread_time = time.time() - start_multi

    print(f"Single-threaded time: {single_thread_time:.4f}s")
    print(f"Multi-threaded time: {multi_thread_time:.4f}s")
    assert len(single_thread_result) == n_sentences
    assert len(multi_thread_result) == n_sentences
    assert len(single_thread_result[0]) == len(multi_thread_result[0])

    # checks if the order is the same
    for i, st_embedding in enumerate(single_thread_result):
        the_same = cosine_similarity(st_embedding, multi_thread_result[i])
        other = cosine_similarity(st_embedding, multi_thread_result[i - 1])
        # the_same is the distance between embedding from single threading and multi threading at the same index
        # this value should be very very very close to one (or rarely 1.0), like 0.9999999....
        # other is the distance between single threading embedding and some other multi threading embedding,
        # which should smaller value than the_same
        print(the_same, other)
        assert other < the_same
