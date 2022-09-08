from pydantic import BaseModel


class UserBase(BaseModel):
    name: str


class User(UserBase):
    userid: int


class UserCreate(UserBase):
    pass


class UserCreateResponse(UserCreate):
    userid: int
