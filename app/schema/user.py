from pydantic import BaseModel
from enum import Enum

class UserType(str, Enum):
    student = "student"
    teacher = "teacher"
    visitor = "visitor"

class UserCreate(BaseModel):
    name: str
    type: UserType

class UserOut(BaseModel):
    id: int
    name: str
    type: UserType
    fines: float

    class Config:
        orm_mode = True
