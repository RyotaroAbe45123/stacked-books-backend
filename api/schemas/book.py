from pydantic import BaseModel
from typing import List, Union


class BookBase(BaseModel):
    isbn: int


class BookRead(BookBase):
    price: int
    pages: int
    author: str
    publisher: str
    title: str


class BookCreate(BookBase):
    price: int
    pages: int
    author: str
    publisher: str
    title: str


class BookCreateResponse(BookCreate):
    pass


# class BookDelete(BookBase):
#     pass
