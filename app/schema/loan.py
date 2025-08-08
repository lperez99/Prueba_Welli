from pydantic import BaseModel
from datetime import date

class LoanCreate(BaseModel):
    user_id: int
    book_id: int

class LoanOut(BaseModel):
    id: int
    user_id: int
    book_id: int
    start_date: date
    end_date: date
    returned: bool
    extended: bool
    status: str

    class Config:
        orm_mode = True
