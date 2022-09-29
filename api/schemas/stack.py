from datetime import datetime
from pydantic import BaseModel
from typing import List, Union


class StackBase(BaseModel):
    isbn: int


class StacksReadResponse(BaseModel):
    timestamp: datetime
    title: str
    price: int
    pages: int


class StackReadResponse(StackBase):
    timestamp: datetime


class StackCreate(StackBase):
    pass


class StackCreateResponse(StackCreate):
    timestamp: datetime


class StackDelete(StackBase):
    pass
