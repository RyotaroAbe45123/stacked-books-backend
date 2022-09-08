from typing import List, Union

from fastapi import HTTPException
from psycopg.rows import class_row

from ..database import get_async_connection
import api.schemas.user as schema


async def read_all_users() -> Union[List[schema.User], List[None]]:
    async with await get_async_connection() as aconn:
        async with aconn.cursor(row_factory=class_row(schema.User)) as acur:
            await acur.execute(
                "SELECT * FROM Users"
            )
            obj = await acur.fetchall()
            return obj if obj else [None]


async def read_user(user_id: int) -> schema.User:
    async with await get_async_connection() as aconn:
        async with aconn.cursor(row_factory=class_row(schema.User)) as acur:
            await acur.execute(
                "SELECT * FROM Users WHERE Users.UserId = %s",
                (user_id,)
            )
            obj = await acur.fetchone()
            if obj is None:
                raise HTTPException(status_code=404, detail='User Not Found')
            return obj


async def create_user(body: schema.UserCreate) -> schema.UserCreateResponse:
    async with await get_async_connection() as aconn:
        async with aconn.cursor(row_factory=class_row(schema.UserCreateResponse)) as acur:
            await acur.execute(
                "INSERT INTO Users (Name) VALUES (%s)",
                (body.name,)
            )
            await acur.execute(
                "SELECT * FROM Users ORDER BY Users.UserId DESC"
            )
            obj = await acur.fetchone()
            return obj


async def update_user(user_id: int, body: schema.UserCreate) -> schema.UserCreateResponse:
    async with await get_async_connection() as aconn:
        async with aconn.cursor(row_factory=class_row(schema.UserCreateResponse)) as acur:
            await acur.execute(
                "UPDATE Users SET Name = %s WHERE Users.UserId = %s",
                (body.name, user_id)
            )
            await acur.execute(
                "SELECT * FROM Users WHERE Users.UserId = %s",
                (user_id,)
            )
            obj = await acur.fetchone()
            return obj


async def delete_user(user_id: int) -> None:
    async with await get_async_connection() as aconn:
        async with aconn.cursor() as acur:
            await acur.execute(
                "DELETE FROM Users WHERE Users.UserId = %s",
                (user_id,)
            )
