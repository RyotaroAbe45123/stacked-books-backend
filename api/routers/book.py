import os
from typing import List, Union

from fastapi import APIRouter, HTTPException, Header

import api.schemas.book as schema
import api.cruds.book as crud_book
import api.cruds.author as crud_author
import api.cruds.subject as crud_subject
from ..utils import get_user_info


router = APIRouter()


def reshape_book(books, authors: list) -> dict:
    result_dict_list = []
    for book in books:
        tmp_authors = [author.author_name for author in authors if author.isbn == book.isbn]
        tmp_dict = dict(**book.dict(), authors=tmp_authors)
        result_dict_list.append(tmp_dict)
    return result_dict_list

@router.get("/books", tags=["book"], response_model=schema.AllBooksReadResponse)
async def read_books(pageSize: int = 3, offset: int = 0, token: str = Header(default=None)):
    user_id = get_user_info(token, os.getenv("IS_LOCAL"))
    books = await crud_book.read_all_books(user_id, pageSize, offset)
    authors = await crud_author.read_authors(user_id)
    books = reshape_book(books, authors)
    count = await crud_book.count_books(user_id)
    return dict(
        data=dict(
            books=books,
            allBooks=count,
        )
    )
    

async def read_book(isbn: int, token: str = Header(default=None)) -> Union[schema.BookReadResponse, None]:
    _ = get_user_info(token, os.getenv("IS_LOCAL"))
    return await crud.read_book(isbn)


async def create_book(body: schema.BookCreate):
    return await crud.create_book(body)
