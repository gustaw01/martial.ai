from nltk.tokenize import sent_tokenize
from nltk.langnames import langname
from itertools import batched
from openai import OpenAI, OpenAIError
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Optional


def create_embeddings(
    text: str, language: str, model_name: str, client: OpenAI
) -> Optional[list[float]]:
    """
    Function to create embeddings from text

    Args:
        text (str): The text to be embedded.
        language (str): The language of the text.
        model_name (str): The OpenAI model to use for embeddings.
        client (OpenAI): The OpenAI API client.

    Returns:
        Optional[List[float]]: A sorted list of embeddings if successful, or None on error.
    """

    sentences = sent_tokenize(text, langname(language).lower())

    try:
        response = client.embeddings.create(input=sentences, model=model_name)
    except OpenAIError as e:
        print(f"OpenAI API returned an error {e}")
        return None

    try:
        embeddings = list(
            map(lambda x: x.embedding, response.data)
        )  # converting response to list of lists of embeddings
    except AttributeError as e:
        print(f"OpenAI API respone without data {e}")
        return None

    return embeddings, sentences


def create_embeddings_multithreading(
    text: str, language: str, model_name: str, client: OpenAI
) -> Optional[List[float]]:
    """
    Function to create embeddings from text with multithreading support.
    Returns a list of floats (vectors) or None if error happened

    Args:
        text (str): The text to be embedded.
        language (str): The language of the text.
        model_name (str): The OpenAI model to use for embeddings.
        client (OpenAI): The OpenAI API client.

    Returns:
        Optional[List[float]]: A sorted list of embeddings if successful, or None on error.
    """

    sentences = sent_tokenize(text, langname(language).lower())
    embeddings = []

    def fetch_embeddings(text_batch, batch_index):
        try:
            response = client.embeddings.create(input=text_batch, model=model_name)
            data = list(map(lambda x: x.embedding, response.data))
            return [(batch_index + i, embedding) for i, embedding in enumerate(data)]
        except (OpenAIError, AttributeError) as e:
            print(f"Error fetching embeddings for batch {batch_index}: {e}")
            return None

    with ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(fetch_embeddings, text_batch, i * 8): i
            for i, text_batch in enumerate(batched(sentences, 8))
        }

        for future in as_completed(futures):
            result = future.result()
            if result:
                embeddings.extend(result)
            else:
                return None  # this is so when an error has happend in fetch_embedding

    return [
        embedding for _, embedding in sorted(embeddings, key=lambda x: x[0])
    ], sentences
