from datetime import datetime
from pydantic import BaseModel
from typing import List, Union


class StackBase(BaseModel):
    isbn: int


class StackReadResponse(StackBase):
    timestamp: datetime
    title: str
    price: Union[int, None]
    pages: Union[int, None]


class StacksReadResponse(StackReadResponse):
    pass


class StackCreate(StackBase):
    pass


class StackCreateResponse(StackCreate):
    timestamp: datetime


class StackDelete(StackBase):
    pass
