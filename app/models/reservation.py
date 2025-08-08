from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from app.database  import Base
import enum
from datetime import datetime, timezone

class StatusReservation(str, enum.Enum):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    status = Column(Enum(StatusReservation), nullable=False, default=StatusReservation.pending)

    user = relationship("User", back_populates="reservations")
    book = relationship("Book", back_populates="reservations")