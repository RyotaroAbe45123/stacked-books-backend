from typing import Union

from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()
# favicon_path = 'favicon.ico'
favicon_path = './book-stack.png'

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/favicon.ico")
def favicon():
    return FileResponse(favicon_path)