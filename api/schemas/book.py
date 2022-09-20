from pydantic import BaseModel
from typing import List, Union


class BookBase(BaseModel):
    isbn: int


class Book(BookBase):
    price: int
    pages: int
    author: str
    publisher: str
    title: str


class BookRead(BookBase):
    pass


class BookCreate(BookBase):
    price: int
    pages: int
    author: str
    publisher: str
    title: str


class BookCreateResponse(BookCreate):
    pass


class BookDelete(BookBase):
    pass
