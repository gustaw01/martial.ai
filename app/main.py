import os
import logging
import json
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from models import Message, MessageResponse, AssessmentRequest, AssessmentResponse
import psycopg2
from dotenv import load_dotenv
from http import HTTPStatus
from typing import List, Optional
from docx import Document
from pypdf import PdfReader
from io import BytesIO
import sys

from algorithm.run_algorithm import run_algorithm

logging.basicConfig(level=logging.DEBUG)
load_dotenv()

app = FastAPI()


def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("PGDATABASE"),
            user=os.getenv("PGUSER"),
            password=os.getenv("PGPASSWORD"),
            host=os.getenv("PGHOST"),
            port=os.getenv("PGPORT", 5432),
        )
        logging.debug("Database connected")
        return conn
    except psycopg2.Error as error:
        logging.error(f"Error connecting to the database \n{error}\nExiting..")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            detail="Database connection error",
        )


@app.get("/")
@app.get("/index")
async def main_route():
    return {"Martial": "AI"}


@app.post("/plagiarism_assessment", response_model=AssessmentResponse)
async def get_plagiarism_assessment(assessment_request: AssessmentRequest):
    """
    Endpoint to create plagiarims assessment for a document/text
    
    """

    file = assessment_request.file
    text = assessment_request.text
    language = assessment_request.language
    author = assessment_request.author
    title = assessment_request.title

    conn = get_db_connection()
    cursor = conn.cursor()

    if file is None and text is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST.value,
            detail="Neither file nor text was probvided"
        )
    elif file is not None and text is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST.value,
            detail="Both file and text was provided"
        )
    
    if file:
        if file.filename.endswith(".pdf"):

            file_content = await file.read()
            pdf_file = BytesIO(file_content)

            reader = PdfReader(pdf_file)
            text = "\n".join([page.extract_text() for page in reader.pages])

            if not text.strip():
                raise HTTPException(
                    status_code=HTTPStatus.UNPROCESSABLE_ENTITY.value,
                    detail="No readable text found in the PDF file.",
                )
            
        elif file.filename.endswith(".docx"):

            document = Document(file.file)
            text = "\n".join([paragraph.text for paragraph in document.paragraphs])

            if not text.strip():
                raise HTTPException(
                    status_code=HTTPStatus.UNPROCESSABLE_ENTITY.value,
                    detail="No readable text found in the DOCX file.",
                )
            
        else:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST.value,
                detail="File format is not accepted",
            )
        

    plagiarism_assessment = run_algorithm(text, language)

    cursor.execute(
        """
        INSERT INTO plagiarisms (title, plagiarism_result, uploaded_text, author)
        VALUES (%s, %s, %s, %s)
        RETURNING id, sent_at
        """,
        (title, json.dumps(plagiarism_assessment), text, author),
    )
    conn.commit()
    assessment_id, sent_at = cursor.fetchone()

    plagiarism_assessment["assessment_id"] = assessment_id
    plagiarism_assessment["sent_at"] = sent_at

    return plagiarism_assessment



@app.post("/history/pdf")
async def read_pdf(
    title: str = Form(...),
    rating: float = Form(...),
    author: str = Form(...),
    file: UploadFile = File(...),
):
    conn = get_db_connection()
    cursor = conn.cursor()

    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST.value,
            detail="Uploaded file must be a PDF file.",
        )

    try:
        file_content = await file.read()
        pdf_file = BytesIO(file_content)

        reader = PdfReader(pdf_file)
        text = ""
        text += "\n".join([page.extract_text() for page in reader.pages])

        if not text.strip():
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY.value,
                detail="No readable text found in the PDF file.",
            )

        cursor.execute(
            """
            INSERT INTO messages (title, rating, message, author)
            VALUES (%s, %s, %s, %s)
            RETURNING id, sent_at
            """,
            (title, rating, text, author),
        )
        conn.commit()
        message_id, sent_at = cursor.fetchone()

        return {
            "id": message_id,
            "sent_at": sent_at,
            "title": title,
            "rating": rating,
            "message": text,
            "author": author,
        }

    except psycopg2.Error as e:
        logging.error(f"Database operation failed: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            detail="Database operation failed",
        )

    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            detail=f"Error processing the PDF file: {str(e)}",
        )


@app.post("/history/docx")
async def read_docx(
    title: str = Form(...),
    rating: float = Form(...),
    author: str = Form(...),
    file: UploadFile = File(...),
):
    conn = get_db_connection()
    cursor = conn.cursor()

    if not file.filename.endswith(".docx"):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST.value,
            detail="Uploaded file must be a DOCX file.",
        )

    try:
        document = Document(file.file)
        text = "\n".join([paragraph.text for paragraph in document.paragraphs])

        if not text.strip():
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY.value,
                detail="No readable text found in the DOCX file.",
            )

        cursor.execute(
            """
            INSERT INTO messages (title, rating, message, author)
            VALUES (%s, %s, %s, %s)
            RETURNING id, sent_at
            """,
            (title, rating, text, author),
        )
        conn.commit()
        message_id, sent_at = cursor.fetchone()

        return {
            "id": message_id,
            "sent_at": sent_at,
            "title": title,
            "rating": rating,
            "message": text,
            "author": author,
        }

    except psycopg2.Error as e:
        logging.error(f"Database operation failed: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            detail="Database operation failed",
        )

    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            detail=f"Error processing the DOCX file: {str(e)}",
        )


@app.post("/history/text")
async def save_history_element(msg: Message):
    conn = get_db_connection()
    cursor = conn.cursor()

    if not (0 <= msg.rating <= 100):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST.value,
            detail="Rating must be between 0 and 100.",
        )
    
    try:
        cursor.execute(
            """
            INSERT INTO messages (title, rating, message, author)
            VALUES (%s, %s, %s, %s)
            RETURNING id, sent_at
            """,
            (msg.title, msg.rating, msg.message, msg.author),
        )
        conn.commit()
        message_id, sent_at = cursor.fetchone()
        return {
            "id": message_id,
            "sent_at": sent_at,
            "title": msg.title,
            "rating": msg.rating,
            "message": msg.message,
            "author": msg.author,
        }
    except psycopg2.Error as e:
        logging.error(f"Database operation failed: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            detail="Database operation failed",
        )
    finally:
        cursor.close()
        conn.close()


@app.get("/history", response_model=List[MessageResponse])
async def get_history_by_author_or_id(
    author: Optional[str] = None, message_id: Optional[int] = None
):
    if not author and not message_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST.value,
            detail="Neither id nor author provided.",
        )

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = "SELECT id, title, rating, message, author, sent_at FROM messages WHERE"
                params = []

                conditions = []
                if author:
                    conditions.append(" author = %s")
                    params.append(author)
                if message_id:
                    conditions.append(" id = %s")
                    params.append(message_id)

                query += " AND ".join(conditions)
                cursor.execute(query, tuple(params))
                messages = cursor.fetchall()

                if not messages:
                    raise HTTPException(
                        status_code=HTTPStatus.NOT_FOUND.value,
                        detail="No messages found.",
                    )

                result = [
                    MessageResponse(
                        id=message[0],
                        title=message[1],
                        rating=message[2],
                        message=message[3],
                        author=message[4],
                        sent_at=message[5].isoformat(),
                    )
                    for message in messages
                ]

                return result

    except HTTPException as http_error:
        raise http_error

    except psycopg2.DatabaseError as db_error:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            detail=f"Database error: {db_error}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            detail=f"Unexpected error: {e}",
        )


@app.delete("/history/{message_id}")
async def delete_history_element(message_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM messages WHERE id = %s;", (message_id,))
        message = cursor.fetchone()

        if not message:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND.value, detail="Message not found"
            )

        cursor.execute("DELETE FROM messages WHERE id = %s;", (message_id,))
        conn.commit()

        return "Deleted successfully."

    except HTTPException as http_error:
        raise http_error

    except Exception as error:
        conn.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value, detail=str(error)
        )

    finally:
        cursor.close()
        conn.close()
