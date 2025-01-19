import os
import logging
import json
from fastapi import FastAPI, HTTPException, UploadFile, Form
from models import AssessmentResponse
import psycopg2
from dotenv import load_dotenv
from http import HTTPStatus
from typing import List, Optional
from docx import Document
from pypdf import PdfReader
from io import BytesIO

from algorithm.run_algorithm import run_algorithm

logging.basicConfig(level=logging.DEBUG)
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
async def get_plagiarism_assessment(
    file: Optional[UploadFile] = None,
    text: Optional[str] = Form(None),
    language: str = Form(...),
    author: str = Form(...),
    title: str = Form(...),
):
    """
    Endpoint to create plagiarims assessment for a document/text
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    if file is None and text is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST.value,
            detail="Neither file nor text was probvided",
        )
    elif file is not None and text == "":
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST.value,
            detail="File is provided but text field is provided with empty string",
        )
    elif file is not None and text is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST.value,
            detail="Both file and text was provided",
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
    plagiarism_assessment["sent_at"] = sent_at.isoformat()
    plagiarism_assessment["author"] = author
    plagiarism_assessment["title"] = title
    plagiarism_assessment["id"] = assessment_id

    return plagiarism_assessment


@app.get("/history", response_model=List[AssessmentResponse])
async def get_history_by_author_or_id(
    author: Optional[str] = None, assessment_id: Optional[int] = None
):
    if not author and not assessment_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST.value,
            detail="Neither id nor author provided.",
        )

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                query = "SELECT * FROM plagiarisms WHERE"
                params = []

                conditions = []
                if author:
                    conditions.append(" author = %s")
                    params.append(author)
                if assessment_id:
                    conditions.append(" id = %s")
                    params.append(assessment_id)

                query += " AND ".join(conditions)
                cursor.execute(query, tuple(params))
                messages = cursor.fetchall()

                if not messages:
                    raise HTTPException(
                        status_code=HTTPStatus.NOT_FOUND.value,
                        detail="No assessment found.",
                    )

                result = []
                for message in messages:
                    id = message[0]
                    title = message[1]
                    plagiarisms_result = message[2]["plagiarisms"]
                    plagiarisms_result_other_lang = message[2]["plagiarisms_other_lang"]
                    rating = message[2]["rating"]
                    rating_other_lang = message[2]["rating_other_lang"]
                    uploaded_text = message[3]
                    author = message[4]
                    sent_at = message[5]

                    result.append(
                        AssessmentResponse(
                            assessment_id=id,
                            title=title,
                            plagiarisms=plagiarisms_result,
                            plagiarisms_other_lang=plagiarisms_result_other_lang,
                            rating=rating,
                            rating_other_lang=rating_other_lang,
                            uploaded_text=uploaded_text,
                            author=author,
                            sent_at=sent_at.isoformat(),
                        )
                    )
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
        cursor.execute("SELECT * FROM plagiarisms WHERE id = %s;", (message_id,))
        message = cursor.fetchone()

        if not message:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND.value, detail="No assessment found."
            )
        cursor.execute("DELETE FROM plagiarisms WHERE id = %s;", (message_id,))
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
