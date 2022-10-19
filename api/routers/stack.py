import os
from typing import List, Union

from fastapi import APIRouter, HTTPException, Header

import api.schemas.stack as schema
import api.cruds.stack as crud_stack
import api.cruds.book as crud_book
import api.cruds.author as crud_author
# import api.cruds.subject as crud_subject
from api.utils import get_user_info
from api.book import Book


router = APIRouter()


@router.get("/stacks", tags=["stack"], response_model=Union[List[schema.StacksReadResponse], List])
async def read_stacks(token: str = Header(default=None)):
    user_id = get_user_info(token, os.getenv("IS_LOCAL"))
    return await crud_stack.read_all_stacks(user_id)


@router.post("/stack", tags=["stack"], response_model=None)
async def create_stack(body: schema.StackCreate, token: str = Header(default=None)):
    user_id = get_user_info(token, os.getenv("IS_LOCAL"))
    stack = await crud_stack.read_stack(user_id, body.isbn)
    if stack is not None:
        raise HTTPException(status_code=500, detail="Stack Existed")

    book = await crud_book.read_book(body.isbn)
    if book is not None:
        print(f'Book Found: {book}')
    else:
        print("Book Not Found. So register it.")
        try:
            book = Book(body.isbn)
            book.search()
            print(f'Book Info: {book.__dict__}')
            await crud_book.create_book(book)
            for author in book.authors:
                await crud_author.create_author(book.isbn, author)            
            # for subject in book.subjects:
            #     await crud_subject.create_subject(book.isbn, subject)            
        except HTTPException as e:
            raise e
    return await crud_stack.create_stack(user_id, body)
    
    
@router.delete("/stack", tags=["stack"], response_model=None)
async def delete_stack(body: schema.StackDelete, token: str = Header(default=None)):
    user_id = get_user_info(token, os.getenv("IS_LOCAL"))
    stack = await crud_stack.read_stack(user_id, body.isbn)
    if stack is None:
        raise HTTPException(status_code=404, detail="Stack Not Found")
    return await crud_stack.delete_stack(user_id, body)
