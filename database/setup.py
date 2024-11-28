import requests
import re
import os
from nltk.tokenize import sent_tokenize
from nltk import download
from itertools import batched
import psycopg2
import logging
from openai import OpenAI
from dotenv import load_dotenv
from http import HTTPStatus

load_dotenv()

logging.basicConfig(
    level=os.getenv("DATABASE_LOGGING_LEVEL", "INFO"), format="%(asctime)s - %(levelname)s - %(message)s", filename="database_setup.log", filemode="a"
)

download("punkt_tab")


def list_wikipedia_titles(search_query: str, n: int = 20, language: str = "en") -> list[str]:
    base_url = f"https://{language}.wikipedia.org/w/api.php"  # language arg to control what language is used
    params = {
        "action": "query",
        "list": "search",
        "srsearch": search_query,
        "format": "json",
        "srlimit": n,
    }

    response = requests.get(base_url, params=params)

    if response.status_code == HTTPStatus.OK:
        data = response.json()
        titles = [(language, item["title"]) for item in data.get("query", {}).get("search", [])]
        logging.debug(f"Found {len(titles)} titles for {search_query}")
        return titles
    else:
        logging.error(f"Getting wiki titles for {search_query} returned code {response.status_code}")
        return []  # ??? or exti


def get_wikipedia_text(page_title: str, language: str = "en") -> str | None:
    url = f"https://{language}.wikipedia.org/w/api.php"

    params = {
        "action": "query",
        "format": "json",
        "prop": "revisions",
        "titles": page_title,
        "rvprop": "content",
        "rvslots": "main",
    }

    response = requests.get(url, params=params)

    if response.status_code == HTTPStatus.OK:
        data = response.json()
        pages = data.get("query", {}).get("pages", {})
        for _, page_content in pages.items():
            try:
                text = page_content["revisions"][0]["slots"]["main"]["*"]
            except KeyError:
                logging.error(f"Unsupported response structure on '{page_title}' page")

            # TEXT CLEANING
            text = re.sub(r"\{\{.*?\}\}", "", text, flags=re.DOTALL)  # double braces
            text = re.sub(r"\{.*?\}", "", text, flags=re.DOTALL)  # remove single braces
            text = re.sub(r"\[\[.*?\|(.*?)\]\]", r"\1", text)  # Keep text
            text = re.sub(r"\[\[.*?\]\]", "", text)  # Remove if no text
            text = re.sub(r"\[http[^\]]+\]", "", text)  # external links
            text = re.sub(r"<.*?>", "", text, flags=re.DOTALL)  # html tags
            text = re.sub(r"File:[^\s]+\s?", "", text, flags=re.IGNORECASE)  # more cleaning
            text = re.sub(r"\s{2,}", " ", text).strip()  # Whitespace

            logging.debug(f"Found {len(text)} chars in '{page_title}' page")
            return text

    else:
        logging.error(f"Getting wiki text for '{page_title}' page returned code {response.status_code}")


def get_embedding_from_sents(texts: list[str], model_name: str, client: OpenAI) -> list[list[float]]:
    try:
        response = client.embeddings.create(input=texts, model=model_name)
        data = list(map(lambda x: x.embedding, response.data))  # converting response to list of lists of embeddings
        logging.info(f"Got {len(data)} vectors from OpenAI API")
        return data

    except Exception as e:
        logging.error(f"An error occurred: {e} while getting OpenAI embeddings")
        return []


def batch_db_upload(
    embeddings: list[list[float]], texts: list[str], title: str, language: str, index_in_doc: list[int], table_name: str, cur
) -> None:
    if len(texts) != len(embeddings):
        logging.error(f"Text and embedding list lenght does not match on article '{title}'")

    columns = ["doc_title", "doc_langauge", "sentence", "embedding", "index_in_doc"]
    data = list(zip([title] * len(texts), [language] * len(texts), texts, embeddings, index_in_doc))
    try:
        # Generate the query dynamically
        columns_str = ", ".join(columns)
        values_placeholder = ", ".join(["%s"] * len(columns))
        query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_placeholder})"

        # Execute the bulk insert
        cur.executemany(query, data)
    except psycopg2.Error as e:
        logging.error(f"Error uploading bulk data: {e}")


ARTS_PER_LANG = 32
DATABASE_TABLE_NAME = "embeddings_test2"

wiki_searches = [["Gwiezdne Wojny", "pl"], ["Star Wars", "en"], ["La Guerre des étoiles", "fr"], ["Star Wars", "tr"]]

nltk_langmap = {"pl": "polish", "en": "english", "fr": "french", "tr": "turkish"}


if __name__ == "__main__":
    logging.info(f"Starting database upload 🤞")

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
        exit()

    model_name = os.getenv("MODEL_NAME")
    logging.info(f"Using {model_name} OpenAI model")
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    for search, language in wiki_searches:
        logging.debug(f"Analzying search '{search}' in language '{language}'")

        for lang_art, title in list_wikipedia_titles(search, ARTS_PER_LANG, language):
            logging.debug(f"Analyzing {title} page in langauage '{language}'")

            wiki_text = get_wikipedia_text(title, lang_art)
            logging.debug(f"Got text from {title} page ({len(wiki_text)} chars) in langauage '{language}'")

            wiki_senetences = sent_tokenize(wiki_text, nltk_langmap[lang_art])
            logging.debug(f"Got sentences from {title} page ({len(wiki_senetences)} sentences) in langauage '{language}'")

            sentence_ind = 0
            for text_batch in batched(wiki_senetences, 32):
                embeddings_batch = get_embedding_from_sents(text_batch, model_name=model_name, client=openai_client)

                # counting sentences in document
                sentences_in_doc = list(range(sentence_ind, sentence_ind + len(text_batch)))
                sentence_ind += len(text_batch)

                batch_db_upload(embeddings_batch, text_batch, title, lang_art, sentences_in_doc, DATABASE_TABLE_NAME, cursor)
                conn.commit()  # commit to actually upload the data

            logging.debug(f"Finishined uploading '{title}' page in langauage '{language}'")

    logging.info(f"Finishined uploading data 🚀")
