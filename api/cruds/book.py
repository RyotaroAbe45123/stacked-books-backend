from typing import List, Union

from fastapi import HTTPException
from psycopg.rows import class_row

from ..database import get_async_connection
import api.schemas.book as schema


async def read_book(isbn: int) -> Union[schema.Book, None]:
    async with await get_async_connection() as aconn:
        async with aconn.cursor(row_factory=class_row(schema.Book)) as acur:
            await acur.execute(
                "SELECT * FROM Books WHERE Books.ISBN = %s",
                (isbn,)
            )
            obj = await acur.fetchone()
            # if obj is None:
            #     raise HTTPException(status_code=404, detail='Book Not Found')
            return obj


async def create_book(body: schema.BookCreate) -> schema.BookCreateResponse:
    async with await get_async_connection() as aconn:
        async with aconn.cursor(row_factory=class_row(schema.BookCreateResponse)) as acur:
            await acur.execute(
                "INSERT INTO Books VALUES (%s, %s, %s, %s, %s, %s)",
                (body.isbn, body.author, body.publisher, body.title, body.price, body.pages)
            )
            return body


async def delete_book(body: schema.BookDelete) -> None:
    async with await get_async_connection() as aconn:
        async with aconn.cursor() as acur:
            await acur.execute(
                "DELETE FROM Books WHERE Books.ISBN = %s",
                (body.isbn,)
            )
