from typing import List, Union

from fastapi import APIRouter, HTTPException, Header

import api.schemas.book as schema
import api.cruds.book as crud
from ..utils import get_user_info


router = APIRouter()


@router.get("/books", tags=["book"], response_model=Union[List[schema.BookRead], List[None]])
async def read_books(token: str = Header(default=None)):
    user_id = get_user_info(token)
    # return schema.Book(**body.dict(), author="author1", publisher="publisher1", title="title1")
    return await crud.read_all_books(user_id)
    

# @router.get("/book", tags=["book"], response_model=Union[schema.Book, None])
async def read_book(isbn: int, token: str = Header(default=None)) -> Union[schema.BookRead, None]:
    _ = get_user_info(token)
    # return schema.Book(**body.dict(), author="author1", publisher="publisher1", title="title1")
    return await crud.read_book(isbn)


# @router.post("/book", response_model=schema.BookCreateResponse)
async def create_book(body: schema.BookCreate):
    # return schema.BookCreateResponse(**body.dict())
    return await crud.create_book(body)
    
    
# @router.delete("/book", response_model=None)
# async def delete_book(body: schema.BookDelete):
#     book = await crud.read_book(body.isbn)
#     if book is None:
#         raise HTTPException(status_code=404, detail="Book Not Found")
#     # return None
#     return await crud.delete_book(body)
