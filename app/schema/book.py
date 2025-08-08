from enum import Enum
from pydantic import BaseModel, field_validator

class BookStatus(str, Enum):
    available = "available"
    borrowed = "borrowed"
    reserved = "reserved"
    maintenance = "maintenance"

class BookCategory(str, Enum):
    fiction = "fiction"
    academic = "academic"
    reference = "reference"
    research = "research"
    history = "history"

class BookBase(BaseModel):
    title: str
    author: str
    category: BookCategory
    status: BookStatus = BookStatus.available
    stock_physical_for_sell: int
    stock_digital: int = -1  
    min_stock_for_sell: int
    price_physical: float
    price_digital: float
    stock_for_loan: int

class BookCreate(BookBase):
    pass


class BookOut(BookBase):
    id: int
    class Config:
        orm_mode = True