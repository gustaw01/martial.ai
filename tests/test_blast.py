from openai import OpenAI
import os
import sys
import time
from dotenv import load_dotenv
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.algorithm.blast import blast, get_sentences_from_doc

load_dotenv(".env")
model_name = os.getenv("MODEL_NAME")
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@pytest.mark.parametrize(
    "target_sentences",
    [
        [
            "2015 saw the premiere of ''The Last Jedi'' (2017) and ''The Rise of Skywalker.",
            "Akcja filmów i innych kanonicznych elementów franczyzy opisuje ponad 60 lat historii.",  # 21
            "W 2015 roku całkowita wartość franczyzy wyniosła 42 mld USD, co pozwoliło zająć jej 2. miejsce wśród najbardziej dochodowych franczyz.",  # 18
            "Akcja utworów należących do ''Legend'' sięga nawet ponad 25 000 lat wstecz, oraz wiek naprzód, opisując niekanoniczną przyszłość w której obca rasa zwana Yuuzhan Vong przybywa z innej galaktyki.",  # 22
            "Nie wiem o czym napisać, pozdrawiam.",
            "Akcja toczy się ''Dawno, dawno temu, w odległej galaktyce…'' Zdanie to pojawia się na początku każdej z części filmu oraz w wielu nawiązaniach.",
        ],
        [
            "2015 saw the premiere of ''The Last Jedi'' (2017) and ''The Rise of Skywalker.",
            "W 2015 roku całkowita wartość franczyzy wyniosła 42 mld USD, co pozwoliło zająć jej 2. miejsce wśród najbardziej dochodowych franczyz.",  # 18
            "Akcja filmów i innych kanonicznych elementów franczyzy opisuje ponad 60 lat historii.",  # 21
            "Akcja utworów należących do ''Legend'' sięga nawet ponad 25 000 lat wstecz, oraz wiek naprzód, opisując niekanoniczną przyszłość w której obca rasa zwana Yuuzhan Vong przybywa z innej galaktyki.",  # 22
            "Nie wiem o czym napisać, pozdrawiam.",
            "Akcja toczy się ''Dawno, dawno temu, w odległej galaktyce…'' Zdanie to pojawia się na początku każdej z części filmu oraz w wielu nawiązaniach.",
        ],
        [""],
        [],
    ],
)
def test_blast(target_sentences):
    target_embeddings = []

    for sentence in target_sentences:
        response = openai_client.embeddings.create(input=sentence, model=model_name)
        target_embeddings.append(response.data[0].embedding)

    doc_title = "Gwiezdne wojny"
    sentences_from_db = get_sentences_from_doc(doc_title)
    start_time = time.time()
    sequences = blast(
        target_embeddings,
        sentences_from_db,
        threshold=0.89,
        max_forward=5,
        max_backward=3,
    )
    duration = time.time() - start_time

    print(f"Found {len(sequences)} sequences in {duration:.5f} seconds.")
    for seq_index, sequence in enumerate(sequences):
        print(f"Sequence {seq_index + 1}:")
        for sentence in sequence:
            print(
                f" ID_target: {sentence['matched_target_id']}, ID_doc: {sentence['sentence_id']}, Similarity: {sentence['similarity']:.2f}"
            )
            print(f"  Text: {sentence['text']}")
        print()
