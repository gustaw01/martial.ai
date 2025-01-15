import sys
import os
from io import BytesIO

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



def test_no_file_or_text():
    response = client.post("/plagiarism_assessment", data={
        "language": "en",
        "author": "Test Author",
        "title": "Test Title"
    })

    assert response.status_code == 400
    assert response.json()["detail"] == "Neither file nor text was probvided"

def test_both_file_and_text():
    response = client.post("/plagiarism_assessment", 
        data={
            "text": "asdfasdfasdf",
            "language": "en",
            "author": "Test Author",
            "title": "Test Title"
    },
    files={"file": ("document.docx", BytesIO(b"asdfasdfasd"), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Both file and text was provided"

def test_upload_pdf():

    data = {
        "language": "en",
        "author": "Author",
        "title": "Title",
    }

    with open(os.path.join("tests", "test_data", "test.pdf"), "rb") as test_file:
        response = client.post(
            "/plagiarism_assessment",
            files={"file": ("document.pdf", test_file, "application/pdf")},
            data=data,
        )

    assert response.status_code == 200
    assert "rating" in response.json() 


def test_docx_file():
    with open(os.path.join("tests", "test_data", "test.docx"), "rb") as test_file:
        response = client.post(
            "/plagiarism_assessment",
            files={"file": ("document.docx", test_file, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
            data={
                "language": "en",
                "author": "Test Author",
                "title": "Test Title",
            },
        )
    assert response.status_code == 200
    assert "rating" in response.json() 

def test_invalid_file_format():
    file_content = BytesIO(b"Sample content")
    response = client.post(
        "/plagiarism_assessment",
        files={"file": ("document.txt", file_content, "text/plain")},
        data={
            "language": "en",
            "author": "Test Author",
            "title": "Test Title",
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "File format is not accepted"

def test_text_submission():
    response = client.post(
        "/plagiarism_assessment",
        data={
            "text": "This is a sample text for plagiarism detection.",
            "language": "en",
            "author": "Test Author",
            "title": "Test Title",
        },
    )
    assert response.status_code == 200
    assert response.json()["rating"] >= 0

def test_empty_pdf_file():
    with open(os.path.join("tests", "test_data", "test_empty.pdf"), "rb") as test_file:
        response = client.post(
            "/plagiarism_assessment",
            data={
                "language": "en",
                "author": "Test Author",
                "title": "Test Title",
            },
            files={"file": ("document.pdf", test_file, "application/pdf")},
        )
    assert response.status_code == 422
    assert response.json()["detail"] == "No readable text found in the PDF file."
