from sqlalchemy.orm import Session
from datetime import date, timedelta
from app.models.loan import Loan, LoanStatus
from app.models.user import User
from app.models.book import Book
from app.schema.loan import LoanCreate

def create_loan(db: Session, data: LoanCreate):
    user = db.query(User).filter(User.id == data.user_id).first()
    book = db.query(Book).filter(Book.id == data.book_id).first()
    
    if not user or not book:
        raise ValueError("Usuario o libro no encontrado.")

    # Validar multas
    if getattr(user, "fines", 0) > 10000:
        raise ValueError("El usuario tiene multas mayores a $10.000. No se puede crear el préstamo.")

    LOAN_DAYS = {"student": 14, "teacher": 30, "visitor": 7}
    MAX_LOANS = {"student": 3, "teacher": 5, "visitor": 1}
    user_type = getattr(user, "type", "visitor")
    loan_days = LOAN_DAYS.get(user_type, 7)
    max_loans = MAX_LOANS.get(user_type, 1)

    # Validar máximo de préstamos activos
    active_loans = db.query(Loan).filter(
        Loan.user_id == user.id,
        Loan.status == LoanStatus.active
    ).count()
    if active_loans >= max_loans:
        raise ValueError(f"El usuario ya alcanzó el máximo de préstamos activos ({max_loans}).")

    # Validar préstamo repetido del mismo libro
    existing_loan = db.query(Loan).filter(
        Loan.user_id == user.id,
        Loan.book_id == book.id,
        Loan.status == LoanStatus.active
    ).first()
    if existing_loan:
        raise ValueError("No puedes prestar el mismo libro dos veces seguidas sin devolverlo.")

    # Validar stock de préstamos
    if book.stock_for_loan < 1:
        raise ValueError("No hay ejemplares físicos disponibles para préstamo.")

    end_date = date.today() + timedelta(days=loan_days)

    loan = Loan(
        user_id=user.id,
        book_id=book.id,
        start_date=date.today(),
        end_date=end_date,
        returned=False,
        extended=False,
        status=LoanStatus.active
    )

    # Disminuir el stock de préstamos
    book.stock_for_loan -= 1
    if book.stock_for_loan == 0:
        book.status = "borrowed"

    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan

def get_loans(db: Session):
    return db.query(Loan).all()

def extend_loan(db, loan_id):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    
    if not loan:
        raise ValueError("Loan not found")
    
    if loan.extended:
        raise ValueError("El prestamo ya ha sido extendido antes, no se puede volver a extender.")
    
    user = db.query(User).filter(User.id == loan.user_id).first()
    
    if not user or user.type != "teacher":
        raise ValueError("Solo los profesores pueden extender el préstamo.")
    from datetime import timedelta
    loan.end_date = loan.end_date + timedelta(days=14)
    loan.extended = True
    db.commit()
    db.refresh(loan)
    return loan


