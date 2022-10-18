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


class BookCreate(BookBase):
    title: str
    pages: int
    c_code: int
    category_code: Union[int, None]
    has_image: bool
    publisher: str
    publish_date: date
    price: int

class BookReadResponse(BookCreate):
    authors: Union[List[str], None]
    subjects: Union[List[str], None]


class BookCreateResponse(BookCreate):
    pass
