from typing import List

import psycopg
from psycopg.rows import class_row
from pydantic import BaseModel

from ..database import DATABASE_URL

class Users(BaseModel):
    userid: int
    name: str


def find_user(user_id: int) -> Users:
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor(row_factory=class_row(Users)) as cur:
            cur.execute(
                "SELECT * FROM Users where Users.UserId = %s",
                (user_id,)
            )
            return cur.fetchone()

def find_users(query: str) -> List[Users]:
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor(row_factory=class_row(Users)) as cur:
            cur.execute(
                query
            )
            return cur.fetchall()

def create_user_record(name: str):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            s = cur.execute(
                "INSERT INTO Users (Name) VALUES (%s)",
                (name,)
            )

def delete_user_record(user_id: int):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            s = cur.execute(
                "DELETE FROM Users where Users.UserId = %s",
                (user_id,)
            )
