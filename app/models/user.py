from sqlalchemy import Column, Integer, String, Float, Enum
from app.database import Base
import enum
from sqlalchemy.orm import relationship

# Definición de tipos de usuario
class UserType(str, enum.Enum):
    student = "student"
    teacher = "teacher"
    visitor = "visitor"

# Modelo de usuario
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    type = Column(Enum(UserType), nullable=False)
    fines = Column(Integer, default=0.0)
    books_on_loan = Column(Integer, default=0)  # Libros actualmente prestados
    loans = relationship("Loan", back_populates="user")
    reservations = relationship("Reservation", back_populates="user")

    def max_books_allowed(self):
        """Devuelve el máximo de libros según el tipo de usuario."""
        limits = {
            UserType.student: 3,
            UserType.teacher: 5,
            UserType.visitor: 1
        }
        return limits[self.type]

    def loan_days_allowed(self):
        """Devuelve la cantidad de días de préstamo según el tipo."""
        days = {
            UserType.student: 14,
            UserType.teacher: 30,
            UserType.visitor: 7
        }
        return days[self.type]