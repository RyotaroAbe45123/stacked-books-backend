from typing import List, Union, Optional

from fastapi import APIRouter, HTTPException, Header

import api.schemas.stack as schema
import api.cruds.stack as crud_stack
import api.cruds.book as crud_book
from ..utils import get_user_info, search_book_info


router = APIRouter()


@router.get("/stacks", response_model=Union[List[schema.Stack], List[None]])
async def read_stacks(token: str = Header(default=None)):
    user_id = get_user_info(token)
    # from datetime import datetime
    # return [schema.Stack(userid=1, isbn=123, timestamp=datetime.now()), schema.Stack(userid=1, isbn=456, timestamp=datetime.now())]
    return await crud_stack.read_all_stacks(user_id)


@router.post("/stack", response_model=schema.StackCreateResponse)
async def create_stack(body: schema.StackCreate, token: str = Header(default=None)):
    user_id = get_user_info(token)
    book = await crud_book.read_book(body.isbn)
    if book is not None:
        print(f'Book Found: {book}')
    else:
        print("Book Not Found. So register it.")
        try:
            book_info = search_book_info(body.isbn)
            print(f'Book Info: {book_info}')
            await crud_book.create_book(book_info)
        except HTTPException as e:
            raise e
    # from datetime import datetime
    # return schema.StackCreateResponse(user_id=user_id, **body.dict(), timestamp=datetime.now())
    return await crud_stack.create_stack(user_id, body)
    
    
@router.delete("/stack", response_model=None)
async def delete_stack(body: schema.StackDelete, token: str = Header(default=None)):
    user_id = get_user_info(token)
    stack = await crud_stack.read_stack(user_id, body)
    if stack is None:
        raise HTTPException(status_code=404, detail="Stack Not Found")
    # return None
    return await crud_stack.delete_stack(user_id, body)
