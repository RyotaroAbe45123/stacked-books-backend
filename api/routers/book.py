from typing import List, Union

from fastapi import APIRouter, HTTPException

import api.schemas.book as schema
import api.cruds.book as crud


router = APIRouter()


@router.get("/book", response_model=Union[schema.Book, None])
# async def read_book(body: schema.BookRead):
async def read_book(isbn: int):
    # return schema.Book(**body.dict(), author="author1", publisher="publisher1", title="title1")
    return await crud.read_book(isbn)


@router.post("/book", response_model=schema.BookCreateResponse)
async def create_book(body: schema.BookCreate):
    # return schema.BookCreateResponse(**body.dict())
    return await crud.create_book(body)
    
    
@router.delete("/book", response_model=None)
async def delete_book(body: schema.BookDelete):
    book = await crud.read_book(body.isbn)
    if book is None:
        raise HTTPException(status_code=404, detail="Book Not Found")
    # return None
    return await crud.delete_book(body)
