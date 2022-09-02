import os
from typing import List

import psycopg
from psycopg.rows import class_row
from pydantic import BaseModel


DATABASE_URL = os.getenv('DATABASE_URL', None)
assert DATABASE_URL is not None, "Not Found DATABASE_URL"


class Books(BaseModel):
    isbn: int
    author: str
    publisher: str
    title: str


def create_book_record(isbn: int):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            author = 'aut'
            publisher = 'pub'
            title = 'tit'
            cur.execute(
                "INSERT INTO Books (ISBN, Author, Publisher, Title) VALUES (%s, %s, %s)",
                (isbn, author, publisher, title)
            )

def delete_book_record(isbn: int):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM Books where Books.ISBN = %s",
                (isbn,)
            )

def get_books_by_user(user_id: int) -> List[Books]:
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor(row_factory=class_row(Books)) as cur:
            cur.execute(
                "SELECT * FROM Stacks LEFT JOIN Books ON Stacks.ISBN = Books.ISBN where Stacks.UserId = %s",
                (user_id,)
            )
            return cur.fetchall()