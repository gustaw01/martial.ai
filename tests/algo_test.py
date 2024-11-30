from algorithm.find_k_nearest import find_k_nearest
from openai import OpenAI
import os


# test for find_k_nearest funtion
def test_find_k_nearest():

    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model_name = os.getenv("MODEL_NAME")

    # This sententeded was translated from Polish into English
    # We are hoping to find the same sentence but in the original language
    translated_sent = "2015 saw the premiere of ''The Last Jedi'' (2017) and ''The Rise of Skywalker."
    org_lang_title = "Gwiezdne wojny"
    org_lang_doc_index = 11

    # embeddings for translated sentece
    response = openai_client.embeddings.create(input=translated_sent, model=model_name)
    vector = response.data[0].embedding

    # calcualating the distance
    test_output = find_k_nearest(vector, 3, "en")

    assert len(test_output) == 3

    # testing if desired text was found
    assert test_output[0][0] == org_lang_title
    assert test_output[0][3] == org_lang_doc_index
    
    # check if ignoring the langauge works 
    assert all(map(lambda x: x[1] != "en", test_output))