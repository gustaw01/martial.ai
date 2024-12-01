import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../app")))

from fastapi.testclient import TestClient
from main import app
from http import HTTPStatus

client = TestClient(app)


def test_main_route():
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"Martial": "AI"}

    response = client.get("/index")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"Martial": "AI"}


def test_save_history_element(valid_message_data):
    response = client.post("/history", json=valid_message_data)
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert "id" in data
    assert data["title"] == valid_message_data["title"]
    assert data["rating"] == valid_message_data["rating"]
    assert data["message"] == valid_message_data["message"]
    assert data["author"] == valid_message_data["author"]


def test_save_history_element_invalid_rating():
    invalid_data = {
        "title": "Invalid Rating Title",
        "rating": 120.0,
        "message": "Invalid message content",
        "author": "Test Author",
    }
    response = client.post("/history", json=invalid_data)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "Rating must be between 0 and 100."


def test_get_history_by_author(valid_message_data):
    client.post("/history", json=valid_message_data)

    response = client.get(f"/history?author={valid_message_data['author']}")
    assert response.status_code == HTTPStatus.OK
    messages = response.json()
    assert len(messages) > 0
    assert messages[0]["author"] == valid_message_data["author"]


def test_get_history_by_id(valid_message_data):
    response = client.post("/history", json=valid_message_data)
    message_id = response.json()["id"]

    response = client.get(f"/history?message_id={message_id}")
    assert response.status_code == HTTPStatus.OK
    message = response.json()[0]
    assert message["id"] == message_id


def test_get_history_no_author_or_id():
    response = client.get("/history")
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()["detail"] == "Neither id nor author provided."


def test_delete_history_element(valid_message_data):
    response = client.post("/history", json=valid_message_data)
    message_id = response.json()["id"]

    response = client.delete(f"/history/{message_id}")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == "Deleted successfully."

    response = client.get(f"/history?message_id={message_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "No messages found."


def test_delete_non_existing_message():
    response = client.delete("/history/9999")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["detail"] == "Message not found"
