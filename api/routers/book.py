from typing import List, Union

from fastapi import APIRouter, HTTPException, Header

import api.schemas.book as schema
import api.cruds.book as crud
from ..utils import get_user_info


router = APIRouter()


@router.get("/books", tags=["book"], response_model=schema.AllBooksReadResponse)
async def read_books(pageSize: int = 3, offset: int = 0, token: str = Header(default=None)):
    user_id = get_user_info(token)
    books = await crud.read_all_books(user_id, pageSize, offset)
    count = await crud.count_books(user_id)
    return dict(
        data=dict(
            books=books,
            allBooks=count,
        )
    )
    

async def read_book(isbn: int, token: str = Header(default=None)) -> Union[schema.BookReadResponse, None]:
    _ = get_user_info(token)
    # return schema.Book(**body.dict(), author="author1", publisher="publisher1", title="title1")
    return await crud.read_book(isbn)


async def create_book(body: schema.BookCreate):
    # return schema.BookCreateResponse(**body.dict())
    return await crud.create_book(body)
