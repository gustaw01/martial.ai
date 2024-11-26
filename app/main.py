import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from dotenv import load_dotenv
from http import HTTPStatus
from typing import List, Optional

logging.basicConfig(level=logging.DEBUG)
load_dotenv()


class MessageCreate(BaseModel):
    message: str
    rating: float
    title: str
    author: str


class MessageResponse(BaseModel):
    id: int
    title: str
    rating: float
    message: str
    author: str
    sent_at: str


app = FastAPI()


class TextPayload(BaseModel):
    text: str


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


@app.post("/history")
async def save_history_element(msg: MessageCreate):
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
        raise HTTPException(status_code=500, detail="Database operation failed")
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
                print(query)
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
            raise HTTPException(status_code=404, detail="Message not found")

        cursor.execute("DELETE FROM messages WHERE id = %s;", (message_id,))
        conn.commit()

        return "Deleted successfully."

    except Exception as error:
        conn.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value, detail=str(error)
        )

    finally:
        cursor.close()
        conn.close()
