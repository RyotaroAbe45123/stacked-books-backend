import os

import psycopg


DATABASE_USER = os.getenv('DATABASE_USER', None)
assert DATABASE_USER is not None, "Not Found DATABASE_USER"
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', None)
assert DATABASE_PASSWORD is not None, "Not Found DATABASE_PASSWORD"
DATABASE_SERVER = os.getenv('DATABASE_SERVER', None)
assert DATABASE_SERVER is not None, "Not Found DATABASE_SERVER"
DATABASE_PORT = os.getenv('DATABASE_PORT', None)
assert DATABASE_PORT is not None, "Not Found DATABASE_PORT"
DATABASE_NAME = os.getenv('DATABASE_NAME', None)
assert DATABASE_NAME is not None, "Not Found DATABASE_NAME"
DATABASE_URL = f"postgres://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_SERVER}:{DATABASE_PORT}/{DATABASE_NAME}"


def get_connection():
    return psycopg.connect(DATABASE_URL)


def get_async_connection():
    return psycopg.AsyncConnection.connect(DATABASE_URL)
