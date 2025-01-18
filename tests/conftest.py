import pytest


@pytest.fixture(scope="module")
def valid_message_data():
    return {
        "text": "This is a sample text for plagiarism detection.",
        "language": "en",
        "author": "Test Author",
        "title": "Test Title",
    }
