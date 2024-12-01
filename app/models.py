from pydantic import BaseModel


class Message(BaseModel):
    message: str
    rating: float
    title: str
    author: str


class MessageResponse(Message):
    id: int
    sent_at: str
