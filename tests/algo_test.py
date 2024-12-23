from openai import OpenAI
import psycopg2
import os
import time
import pytest
import sys
import dotenv
from nltk import download, sent_tokenize
from nltk.langnames import langname
import math

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../algorithm")))
dotenv.load_dotenv()

from find_k_nearest import find_k_nearest
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


TEST_TEXT = """
The cat jumped over the tall wooden fence.
A spaceship landed quietly in the backyard.
She painted the sky in hues of lavender and gold.
The clock struck midnight as the wolves began to howl.
He accidentally spilled coffee on his favorite book.
A vibrant rainbow appeared after the thunderstorm.
The library was silent except for the rustle of pages turning.
Suddenly, the lights in the house flickered and went out.
The child stared in awe at the giant Ferris wheel.
A mysterious letter arrived at her doorstep one morning.
The chef carefully diced the onions with precision.
His laughter echoed through the vast empty canyon.
The waves crashed against the rocks with a deafening roar.
She found a hidden key buried in the flowerbed.
The old man told stories of dragons and magical kingdoms.
A single red rose bloomed amidst the desert sands.
The sound of distant bagpipes carried through the foggy valley.
The robot greeted them with a cheerful "Hello, human!"
A gentle breeze carried the scent of jasmine across the garden.
He discovered a treasure map hidden inside an ancient book.
A comet streaked across the night sky, leaving a fiery trail.
The mysterious artifact hummed softly in the archaeologist’s hands.
A cat perched on the roof, gazing at the moon.
The distant hum of machinery filled the air.
Her eyes sparkled like diamonds as she smiled.
An army of ants marched in a perfect line across the counter.
The chocolate melted slowly in the summer sun.
The wind whispered secrets through the trees.
A firefly glowed brightly in the pitch-black night.
He whistled a tune while riding his bicycle down the hill.
The carnival was alive with colorful lights and cheerful music.
She found solace in the rhythm of the ocean waves.
A knight in shining armor approached the castle gates.
The scent of fresh bread wafted from the bakery.
They watched as a kite soared high into the blue sky.
An owl hooted softly from its perch on the tree branch.
He sketched a portrait of the bustling city from memory.
The glass shattered into a thousand sparkling pieces.
A child’s laughter echoed across the playground.
The abandoned house was cloaked in shadows and mystery.
She danced barefoot in the meadow under the moonlight.
The scientist gazed at the swirling galaxies through the telescope.
A clock ticked rhythmically in the corner of the room.
The aroma of freshly brewed coffee filled the air.
He climbed to the peak and shouted, “I made it!”
A dragonfly hovered over the still surface of the pond.
The detective examined the footprints leading into the forest.
She jotted down notes in her journal by candlelight.
A lone wolf stood on the ridge, silhouetted against the sunset.
The crowd erupted into applause as the curtain fell.
The rain began to pour as they huddled under the umbrella.
The magician pulled a rabbit from his hat, to everyone’s amazement.
He carefully wrapped the gift in shiny gold paper.
The classroom buzzed with the chatter of eager students.
A balloon popped suddenly, startling the group.
The lighthouse stood resolute, guiding ships to safety.
She read the note aloud, her voice trembling with emotion.
The butterfly flitted gracefully among the wildflowers.
He built a snowman with a crooked carrot nose.
The fisherman reeled in a catch that sparkled in the sunlight.
The chandelier swayed slightly during the tremor.
A trail of breadcrumbs led deeper into the dark woods.
The sun peeked through the curtains, warming her face.
The roar of a jet engine shattered the calm morning.
She opened the box to find a sparkling necklace inside.
The puppy wagged its tail furiously at the sight of its owner.
The artist splattered paint across the canvas with abandon.
A gentle rain began to patter against the windowpane.
The astronaut floated weightlessly inside the spacecraft.
The campfire crackled as the group shared ghost stories.
A squirrel darted up the tree, clutching an acorn in its mouth.
The distant mountains were blanketed in a layer of mist.
The old vinyl record played a tune from decades past.
She traced the constellation patterns in the night sky.
The buzzing of bees filled the sunlit meadow.
He discovered a secret passage behind the bookcase.
The train whistle echoed across the vast plains.
The aroma of roasted marshmallows lingered in the air.
A ship sailed steadily across the horizon at dawn.
The kitten curled up on the warm blanket, purring softly.
The festival was alive with the sounds of laughter and music.
A crack of thunder startled the flock of birds into flight.
The detective pieced together clues to solve the mystery.
The waterfall cascaded into the crystal-clear pool below.
The rusty gate creaked as it swung open.
A lone figure walked across the frozen lake, leaving faint footprints.
The candy shop was filled with bright colors and sweet smells.
The hiker paused to admire the breathtaking view from the summit.
She scribbled her thoughts onto a napkin in a crowded café.
The roaring fire in the hearth chased away the winter chill.
A flock of geese flew in a perfect V formation overhead.
The old photograph faded with time but held precious memories.
He played a haunting melody on the grand piano.
The sunflowers swayed gently in the summer breeze.
The scent of pine trees filled the crisp mountain air.
The sound of waves lulled her into a peaceful sleep.
A meteor shower lit up the sky in a dazzling display.
The door creaked open to reveal a forgotten attic.
He planted a tiny seedling in the fertile soil.
The echo of her voice lingered long after she had spoken.
"""


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

    # This sententeded was translated from Polish into English
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
