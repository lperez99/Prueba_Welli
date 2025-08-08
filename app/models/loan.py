from sqlalchemy import Column, Integer, ForeignKey, Date, Boolean
from sqlalchemy import Enum as SAEnum
from enum import Enum
from sqlalchemy.orm import relationship
from datetime import date
from app.database import Base

class LoanStatus(str, Enum):
    active = "active"
    returned = "returned"
    extended = "extended"
    late = "late"

class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))

    start_date = Column(Date, default=date.today)
    end_date = Column(Date)
    returned = Column(Boolean, default=False)
    extended = Column(Boolean, default=False)
    status = Column(SAEnum(LoanStatus), default=LoanStatus.active)

    user = relationship("User", back_populates="loans")
    book = relationship("Book", back_populates="loans")
