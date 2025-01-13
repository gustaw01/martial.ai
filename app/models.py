from pydantic import BaseModel
from fastapi import UploadFile


class Message(BaseModel):
    message: str
    rating: float
    title: str
    author: str


class MessageResponse(Message):
    id: int
    sent_at: str


class AssessmentRequest(BaseModel):
        author: str
        language: str
        title: str = ""
        text: str|None = None
        file: UploadFile|None = None
