from datetime import datetime, timedelta, timezone
from typing import List

import psycopg
from psycopg.rows import class_row
from pydantic import BaseModel

from ..database import DATABASE_URL

class Stacks(BaseModel):
    userid: int
    isbn: int


def create_stack_record(user_id: int, isbn: int):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            jst = timezone(timedelta(hours=+9), "JST")
            timestamp = datetime.now(jst).isoformat(timespec="seconds")
            cur.execute(
                "INSERT INTO Stacks (UserId, ISBN, TimeStamp) VALUES (%s, %s, %s)",
                (user_id, isbn, timestamp)
            )

def delete_stack_record(user_id: int, isbn: int):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM Stacks where Stacks.UserId = %s AND Stacks.ISBN = %s",
                (user_id, isbn)
            )

def get_stacks(user_id: int) -> List[Stacks]:
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor(row_factory=class_row(Stacks)) as cur:
            cur.execute(
                "SELECT * FROM Stacks where Stacks.UserId = %s",
                (user_id,)
            )
            return cur.fetchall()

def get_stacks_num(user_id: int):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT COUNT(*) FROM Stacks where Stacks.UserId = %s",
                (user_id,)
            )
            return cur.fetchone()