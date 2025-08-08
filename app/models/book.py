from sqlalchemy import Column, Integer, String, Enum, Float
from app.database import Base
import enum

class BookStatus(str, enum.Enum):
    available = "available"
    borrowed = "borrowed"
    reserved = "reserved"
    maintenance = "maintenance"

class BookCategory(str, enum.Enum):
    fiction = "fiction"
    academic = "academic"
    reference = "reference"
    research = "research"
    history = "history"

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    category = Column(Enum(BookCategory), nullable=False)
    status = Column(Enum(BookStatus), default=BookStatus.available)

    # Inventario
    stock_physical = Column(Integer, default=0)
    stock_digital = Column(Integer, default=0)
    min_stock = Column(Integer, default=1)  # Punto de reorden

    # Precios
    price_physical = Column(Float, nullable=False)
    price_digital = Column(Float, nullable=False)