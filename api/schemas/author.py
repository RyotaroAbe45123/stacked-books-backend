from pydantic import BaseModel


class AuthorBase(BaseModel):
    author_name: str

