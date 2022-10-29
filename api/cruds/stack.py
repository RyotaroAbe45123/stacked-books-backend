from datetime import datetime, timedelta, timezone
from typing import List, Union

from fastapi import HTTPException
from psycopg.rows import class_row

from ..database import get_async_connection
import api.schemas.stack as schema


async def read_all_stacks(user_id: int) -> Union[List[schema.StacksReadResponse], List]:
    async with await get_async_connection() as aconn:
        async with aconn.cursor(row_factory=class_row(schema.StacksReadResponse)) as acur:
            await acur.execute(
                "SELECT s.isbn, timestamp, title, price, pages, c_code \
                    FROM Stacks AS S \
                        LEFT JOIN Books AS B ON S.ISBN = B.ISBN \
                            WHERE S.UserId = %s \
                                ORDER BY timestamp DESC",
                (user_id,)
            )
            return await acur.fetchall()


async def read_stack(user_id: int, isbn: int) -> Union[schema.StackReadResponse, None]:
    async with await get_async_connection() as aconn:
        async with aconn.cursor(row_factory=class_row(schema.StackReadResponse)) as acur:
            await acur.execute(
                "SELECT isbn, timestamp FROM Stacks WHERE Stacks.UserId = %s AND Stacks.ISBN = %s",
                (user_id, isbn)
            )
            return await acur.fetchone()


async def create_stack(user_id: int, body: schema.StackCreate) -> None:
    async with await get_async_connection() as aconn:
        async with aconn.cursor() as acur:
            jst = timezone(timedelta(hours=+9), "JST")
            timestamp = datetime.now(jst).isoformat(timespec="seconds")
            await acur.execute(
                "INSERT INTO Stacks (UserId, ISBN, TimeStamp) VALUES (%s, %s, %s)",
                (user_id, body.isbn, timestamp)
            )


async def delete_stack(user_id: int, body: schema.StackDelete) -> None:
    async with await get_async_connection() as aconn:
        async with aconn.cursor() as acur:
            await acur.execute(
                "DELETE FROM Stacks WHERE Stacks.UserId = %s AND Stacks.ISBN = %s",
                (user_id, body.isbn)
            )
