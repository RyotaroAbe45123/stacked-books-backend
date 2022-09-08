from pydantic import BaseModel
from typing import List, Union


class BookBase(BaseModel):
    isbn: int


class Book(BookBase):
    author: str
    publisher: str
    title: str


class BookRead(BookBase):
    pass


class BookCreate(BookBase):
    author: str
    publisher: str
    title: str


class BookCreateResponse(BookCreate):
    pass


class BookDelete(BookBase):
    pass
