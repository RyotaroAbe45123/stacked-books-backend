from datetime import datetime
from pydantic import BaseModel
from typing import List, Union


class Stacks(BaseModel):
    timestamp: datetime
    price: int
    pages: int

class StackBase(BaseModel):
    isbn: int


class Stack(StackBase):
    timestamp: datetime


class StackRead(StackBase):
    pass


class StackCreate(StackBase):
    pass


class StackCreateResponse(StackCreate):
    timestamp: datetime


class StackDelete(StackBase):
    pass
