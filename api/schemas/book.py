from datetime import datetime, date
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


class BookReadResponse(BookBase):
    price: int
    pages: int
    author: str
    publisher: str
    title: str
    subjects: Union[List[str], None]


class BookCreate(BookBase):
    title: str
    pages: int
    c_code: int
    category_code: int
    has_image: bool
    publisher: str
    publish_date: date
    price: int


class BookCreateResponse(BookCreate):
    pass
