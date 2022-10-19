from pydantic import BaseModel


class AuthorBase(BaseModel):
    isbn: int
    author_name: str

