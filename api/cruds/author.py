from ..database import get_async_connection


async def create_author(isbn: int, author_name: str):
    async with await get_async_connection() as aconn:
        async with aconn.cursor() as acur:
            await acur.execute(
                "INSERT INTO Authors VALUES (%s, %s)",
                (isbn, author_name)
            )