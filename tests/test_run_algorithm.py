import time
import pytest
import sys
import dotenv
import os
from test_data import TEST_TEXT

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../algorithm")))
dotenv.load_dotenv()

from run_algorithm import run_algorithm


@pytest.mark.parametrize(
        "text, language",
        [(TEST_TEXT, "en")]
    )
def test_run_algorithm(text, language):
    plagiarisms, plagiarisms_other_lang = run_algorithm(text, language)


    print(plagiarisms)
