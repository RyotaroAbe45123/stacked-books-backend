from typing import List, Union

from psycopg.rows import class_row

import api.schemas.author as schema
from ..database import get_async_connection


async def read_authors(user_id: int) -> Union[List[schema.AuthorBase], List]:
    async with await get_async_connection() as aconn:
        async with aconn.cursor(row_factory=class_row(schema.AuthorBase)) as acur:
            await acur.execute(
                "SELECT S.isbn, author_name \
                    FROM Stacks AS S \
                        LEFT JOIN Authors AS A ON S.ISBN = A.ISBN \
                            WHERE S.UserId = %s",
                (user_id,)
            )
            return await acur.fetchall()


async def create_author(isbn: int, author_name: str):
    async with await get_async_connection() as aconn:
        async with aconn.cursor() as acur:
            await acur.execute(
                "INSERT INTO Authors VALUES (%s, %s)",
                (isbn, author_name)
            )