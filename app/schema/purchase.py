from pydantic import BaseModel
from datetime import datetime

class PurchaseCreate(BaseModel):
    user_id: int
    book_id: int
    quantity: int
    type: str  # "physical" o "digital"

class PurchaseOut(PurchaseCreate):
    id: int
    total_price: float
    created_at: datetime

    class Config:
        from_attributes = True