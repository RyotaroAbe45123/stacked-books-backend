import os
from typing import Union

from fastapi import FastAPI
from fastapi.responses import FileResponse
import psycopg2

app = FastAPI()
favicon_path = './book-stack.png'

DATABASE_URL = os.getenv('DATABASE_URL', None)
print(DATABASE_URL)


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/users")
def get_data():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    table_name = "Users"
    query = f"SELECT * FROM {table_name}"
    cur.execute(query)
    result = cur.fetchall()
    print(result)
    cur.close()
    conn.close()
    return {"data": f'{result}'}

@app.get("/stacks")
def get_data():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    table_name = "Stacks"
    query = f"SELECT * FROM {table_name}"
    cur.execute(query)
    result = cur.fetchall()
    print(result)
    cur.close()
    conn.close()
    return {"data": f'{result}'}

@app.get("/books")
def get_data():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    table_name = "Books"
    query = f"SELECT * FROM {table_name}"
    cur.execute(query)
    result = cur.fetchall()
    print(result)
    cur.close()
    conn.close()
    return {"data": f'{result}'}

@app.get("/favicon.ico")
def favicon():
    return FileResponse(favicon_path)

