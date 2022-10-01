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

class AllBooksReadResponse(BaseModel):
    data: dict
    # data: {
    #     "books": List[BooksReadResponse],
    #     "allBooks": int
    # }


class BookReadResponse(BookBase):
    price: int
    pages: int
    author: str
    publisher: str
    title: str
    subjects: Union[List[str], None]


class BookCreate(BookBase):
    price: int
    pages: int
    author: str
    publisher: str
    title: str


class BookCreateResponse(BookCreate):
    pass
