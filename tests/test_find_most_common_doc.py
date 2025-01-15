
import pytest
import sys
import dotenv
import os
from openai import OpenAI
import psycopg2

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../algorithm")))
dotenv.load_dotenv()

from find_most_common_docs import find_most_common_docs
from create_embeddings import create_embeddings

def test_find_most_common_doc():


    text = """
        'Równocześnie młodzieniec kuszony jest przez zło (uosabiane przez mroczną postać Dartha Sidiousa), które odwołuje się do jego ambicji i podsyca je, aby ostatecznie zawrzeć „szatański pakt” – poddanie się mu za cenę zaspokojenia własnych pragnień i posiadania wszechmocy, która okazuje się złudna.'
        Dobro i Zło są w ''Gwiezdnych wojnach'' przedstawione jednoznacznie, jednak nie oznacza to, że opisywany świat jest czarno-biały: nawet Jedi (w tym Mistrz Yoda) mają swoje słabości.
        Nawet Vader nie jest w istocie zły, jest zwyczajnym człowiekiem, który uległ powabom zła.
        ''Gwiezdne wojny'' to opowieść o sile tkwiącej w miłości: to, czego nie mogli dokonać najwięksi i najpotężniejsi Rycerze Jedi – pokonanie Sithów – dokonuje się dzięki miłości syna do ojca oraz ojca do syna.
    """

    model = os.getenv("MODEL_NAME")
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    lang = "pl"
    embeddings, _ = create_embeddings(text, lang, model, openai_client)

    conn = psycopg2.connect(
        dbname=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        host=os.getenv("PGHOST"),
        port=os.getenv("PGPORT", 5432),
    )

    vec_lenght = int(os.getenv("VECTOR_LENGTH"))
    most_common_docs = find_most_common_docs(embeddings, 3, conn, vec_lenght, lang)
    print(most_common_docs)