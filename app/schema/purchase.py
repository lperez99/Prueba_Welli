from pydantic import BaseModel
from datetime import datetime

class PurchaseCreate(BaseModel):
    user_id: int
    book_id: int
    quantity: int
    type: str  # "physical" o "digital"
    status: str = "pending"  # "pending", "completed", "cancelled"
    reserved_until: datetime | None = None

class PurchaseOut(PurchaseCreate):
    id: int
    total_price: float
    created_at: datetime

    class Config:
        from_attributes = True