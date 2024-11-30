import pytest


@pytest.fixture(scope="module")
def valid_message_data():
    return {
        "title": "Test Title",
        "rating": 85.0,
        "message": "Test message content",
        "author": "Test Author",
    }
