from typing import List, Union

from psycopg.rows import class_row

import api.schemas.subject as schema
from ..database import get_async_connection


async def read_subjects(isbn: int) -> Union[List[schema.SubjectBase], List]:
    async with await get_async_connection() as aconn:
        async with aconn.cursor(row_factory=class_row(schema.SubjectBase)) as acur:
            await acur.execute(
                "SELECT keyword FROM Subjects Where Subjects.ISBN = %s",
                (isbn,)
            )
            return await acur.fetchall()
            obj = await acur.fetchall()
            return obj


async def create_subject(isbn: int, keyword: str) -> None:
    async with await get_async_connection() as aconn:
        async with aconn.cursor() as acur:
            await acur.execute(
                "INSERT INTO Subjects VALUES (%s, %s)",
                (isbn, keyword)
            )
