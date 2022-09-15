from datetime import datetime, timedelta, timezone
from typing import List, Union

from fastapi import HTTPException
from psycopg.rows import class_row

from ..database import get_async_connection
import api.schemas.stack as schema


async def read_all_stacks(user_id: int) -> Union[List[schema.Stack], List[None]]:
    async with await get_async_connection() as aconn:
        async with aconn.cursor(row_factory=class_row(schema.Stack)) as acur:
            await acur.execute(
                "SELECT * FROM Stacks WHERE Stacks.UserId = %s",
                (user_id,)
            )
            obj = await acur.fetchall()
            return obj if obj else [None]


async def read_stack(body: schema.StackRead) -> schema.Stack:
    async with await get_async_connection() as aconn:
        async with aconn.cursor(row_factory=class_row(schema.Stack)) as acur:
            await acur.execute(
                "SELECT * FROM Stacks WHERE Stacks.UserId = %s AND Stacks.ISBN = %s",
                (body.userid, body.isbn)
            )
            obj = await acur.fetchone()
            if obj is None:
                raise HTTPException(status_code=404, detail='User Not Found')
            return obj


async def create_stack(body: schema.StackCreate) -> schema.StackCreateResponse:
    async with await get_async_connection() as aconn:
        async with aconn.cursor(row_factory=class_row(schema.StackCreateResponse)) as acur:
            jst = timezone(timedelta(hours=+9), "JST")
            timestamp = datetime.now(jst).isoformat(timespec="seconds")
            await acur.execute(
                "INSERT INTO Stacks (UserId, ISBN, TimeStamp) VALUES (%s, %s, %s)",
                (body.userid, body.isbn, timestamp)
            )
            await acur.execute(
                "SELECT * FROM Stacks ORDER BY Stacks.TimeStamp DESC"
            )
            obj = await acur.fetchone()
            return obj


async def delete_stack(body: schema.StackDelete) -> None:
    async with await get_async_connection() as aconn:
        async with aconn.cursor() as acur:
            await acur.execute(
                "DELETE FROM Stacks WHERE Stacks.UserId = %s AND Stacks.ISBN = %s",
                (body.userid, body.isbn)
            )