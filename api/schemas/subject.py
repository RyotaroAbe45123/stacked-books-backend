from pydantic import BaseModel


class SubjectBase(BaseModel):
    subject: str

