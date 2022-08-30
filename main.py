import os
from typing import Union

from fastapi import FastAPI
from fastapi.responses import FileResponse
import psycopg2

app = FastAPI()
favicon_path = './book-stack.png'

DATABASE_URL = os.getenv('DATABASE_URL', None)
print(DATABASE_URL)
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/db")
def get_data():
    query = "SELECT * FROM Users"
    cur.execute(query)
    result = cur.fetchone()
    print(result)
    cur.close()
    conn.close()

    return {"data": f'{result}'}

@app.get("/favicon.ico")
def favicon():
    return FileResponse(favicon_path)

