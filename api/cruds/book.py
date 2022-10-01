from typing import List, Union

from fastapi import HTTPException
from psycopg.rows import class_row

from ..database import get_async_connection
import api.schemas.book as schema


async def read_all_books(user_id: int, pageSize: int, offset: int) -> Union[List[schema.BooksReadResponse], List]:
    async with await get_async_connection() as aconn:
        async with aconn.cursor(row_factory=class_row(schema.BooksReadResponse)) as acur:
            await acur.execute(
                "SELECT S.ISBN, author, publisher, title, price, pages \
                    FROM Stacks AS S \
                        LEFT JOIN Books AS B ON S.ISBN = B.ISBN \
                        WHERE S.UserId = %s \
                            ORDER BY TimeStamp desc \
                            LIMIT %s \
                            OFFSET %s",
                (user_id, pageSize, offset)
            )
            obj = await acur.fetchall()
            return obj if obj else []


async def count_books(user_id) -> int:
    async with await get_async_connection() as aconn:
        async with aconn.cursor() as acur:
            await acur.execute(
                "SELECT COUNT(*) \
                    FROM Stacks AS S \
                        LEFT JOIN Books AS B ON S.ISBN = B.ISBN \
                        WHERE S.UserId = %s",
                (user_id,)
            )
            count = await acur.fetchone()
            return count if count else 0


async def read_book(isbn: int) -> Union[schema.BookReadResponse, None]:
    async with await get_async_connection() as aconn:
        async with aconn.cursor(row_factory=class_row(schema.BookReadResponse)) as acur:
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
