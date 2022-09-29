from datetime import datetime
from pydantic import BaseModel
from typing import List, Union


class BookBase(BaseModel):
    isbn: int


class BooksReadResponse(BookBase):
    price: int
    pages: int
    author: str
    publisher: str
    title: str


class BookReadResponse(BookBase):
    price: int
    pages: int
    author: str
    publisher: str
    title: str
    subjects: List[str]


class BookCreate(BookBase):
    price: int
    pages: int
    author: str
    publisher: str
    title: str


class BookCreateResponse(BookCreate):
    pass
