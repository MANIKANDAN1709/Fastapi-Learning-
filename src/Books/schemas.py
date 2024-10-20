from beanie import Document
from pydantic import BaseModel


class Book_Input(BaseModel):
    title: str


class Book(Document):
    title: str
