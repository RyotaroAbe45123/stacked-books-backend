from datetime import datetime, date
from pydantic import BaseModel
from typing import List, Union


class BookBase(BaseModel):
    isbn: int

class AllBooksReadResponse(BaseModel):
    data: dict

class BookCreate(BookBase):
    title: str
    pages: Union[int, None]
    c_code: Union[str, None]
    category_code: Union[str, None]
    has_image: bool
    publisher: str
    publish_date: Union[date, None]
    price: Union[int, None]

class BooksReadResponse(BookCreate):
    pass

class BookReadResponse(BookCreate):
    authors: Union[List[str], None]
    # subjects: Union[List[str], None]

class BookCreateResponse(BookCreate):
    pass
