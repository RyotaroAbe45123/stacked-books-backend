from typing import List, Union

import api.schemas.subject as schema
from ..database import get_async_connection


async def read_subjects(isbn: int) -> Union[List[schema.SubjectBase], List[None]]:
    async with await get_async_connection() as aconn:
        # async with aconn.cursor() as acur:
        async with aconn.cursor(row_factory=class_row(schema.SubjectBase)) as acur:
            await acur.execute(
                "SELECT subject FROM Subjects Where Subjects.ISBN = %s",
                (isbn,)
            )
            obj = await acur.fetchall()
            return obj


async def create_subject(isbn: int, subject: str):
    async with await get_async_connection() as aconn:
        async with aconn.cursor() as acur:
        # async with aconn.cursor(row_factory=class_row(schema.BookCreateResponse)) as acur:
            await acur.execute(
                "INSERT INTO Subjects VALUES (%s, %s)",
                (isbn, subject)
            )
