from pydantic import BaseModel
from datetime import datetime

class ReservationBase(BaseModel):
    user_id: int
    book_id: int
    status: str

class ReservationCreate(ReservationBase):
    pass

class ReservationOut(ReservationBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True 