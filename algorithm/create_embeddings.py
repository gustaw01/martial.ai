from nltk.tokenize import sent_tokenize
from nltk.langnames import langname
from itertools import batched
from nltk import download
from openai import OpenAI, OpenAIError


download("punkt_tab")


def create_embeddings(text: str, language: str, model_name: str, client: OpenAI) -> list[float] | None:
    """
    Function to create embeddings from a paragraph of text

    text: str
    language: str
    model_name: str
    client: openai.OpenAI


    """

    sentences = sent_tokenize(text, langname(language))
    embeddings = []
    for i, text_batch in enumerate(batched(sentences, 32)):
        index = range(i, len(text_batch))

        try:
            response = client.embeddings.create(input=text_batch, model=model_name)
        except OpenAIError as e:
            print(f"OpenAI API returned an error {e}")
            return None

        try:
            data = list(map(lambda x: x.embedding, response.data))  # converting response to list of lists of embeddings
        except AttributeError as e:
            print(f"OpenAI API respone without data {e}")
            return None

        embeddings.extend(zip(index, data))

    return sorted(embeddings, lambda x: x[0])
