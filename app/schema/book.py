

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
    stock_physical: int
    stock_digital: str = "infinite"  # Default to "infinite" for digital stock
    min_stock: int
    price_physical: float
    price_digital: float


class BookCreate(BookBase):
    pass


class BookOut(BookBase):
    id: int
    
    @field_validator("stock_digital", mode="before")
    def handle_infinite_stock(cls, value):
        return "infinite" if value == -1 else value

    class Config:
        orm_mode = True