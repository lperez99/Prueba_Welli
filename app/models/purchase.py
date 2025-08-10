from app.database import Base
from sqlalchemy import Column, Integer, Float, ForeignKey, String, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.services import reservation

class PurchaseStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"  
    rejected = "rejected"
class PurchaseType(str, enum.Enum):
    physical = "physical"
    digital = "digital"

class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    type = Column(Enum(PurchaseType), nullable=False)
    status = Column(Enum(PurchaseStatus), default=PurchaseStatus.pending)
    created_at = Column(DateTime, default=datetime.utcnow)
    reserved_until = Column(DateTime, nullable=True)

    user = relationship("User")
    book = relationship("Book")