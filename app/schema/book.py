

from enum import Enum
from pydantic import BaseModel


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
    stock_digital: int
    min_stock: int
    price_physical: float
    price_digital: float


class BookCreate(BookBase):
    pass


class BookOut(BookBase):
    id: int

    class Config:
        orm_mode = True