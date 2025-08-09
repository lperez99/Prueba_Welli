from sqlalchemy.orm import Session
from datetime import date, timedelta
from app.models.loan import Loan, LoanStatus
from app.models.user import User
from app.models.book import Book
from app.models.reservation import Reservation
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

    
    if book.stock_for_loan < 1:
        existing_reservation = db.query(Reservation).filter(
            Reservation.user_id == user.id,
            Reservation.book_id == book.id
        ).first()
        if existing_reservation:
            raise ValueError("Ya tienes una reserva activa para este libro.")
        
        reservation = Reservation(user_id=user.id, book_id=book.id)
        db.add(reservation)
        db.commit()
        raise ValueError("No hay ejemplares disponibles. Se ha creado una reserva para este libro.")
    
    pending_reservation = db.query(Reservation).filter(
        Reservation.book_id == book.id
    ).order_by(Reservation.created_at.asc()).first()

    if pending_reservation:
        raise ValueError("Este libro tiene reservas pendientes. No se puede prestar directamente.")
    
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
        raise ValueError("Prestamo no encontrado")
    
    if loan.status != LoanStatus.active:
        raise ValueError("El préstamo no está activo, no se puede extender.")
    
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

def return_loan(db: Session, loan_id: int):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise ValueError("Préstamo no encontrado")

    # Permitir devolver si está activo o late
    if loan.status not in [LoanStatus.active, LoanStatus.late]:
        print(f"El préstamo ya está marcado como devuelto. {loan.status} ")
        raise ValueError("El préstamo no está activo")

    # --- LÓGICA DE MULTA POR RETRASO ---
    today = date.today()
    fine = 0
    if today > loan.end_date:
        days_late = (today - loan.end_date).days
        fine = days_late * 2000
        user = db.query(User).filter(User.id == loan.user_id).first()
        user.fines += fine
        fine_str = f"{fine:,.0f}".replace(",", ".")
        print(f"⚠️ El usuario {user.name} tiene una multa de ${fine_str} por {days_late} días de retraso. Se ha aplicado la multa a su cuenta.")

    loan.status = LoanStatus.returned
    loan.returned = True

    book = db.query(Book).filter(Book.id == loan.book_id).first()
    if not book:
        raise ValueError("Libro no encontrado")

    
    
    # Buscar la reserva más antigua para este libro
    reservation = db.query(Reservation).filter(
        Reservation.book_id == book.id
    ).order_by(Reservation.created_at.asc()).first()

    if reservation:
        # Crear préstamo para el usuario con reserva
        user = db.query(User).filter(User.id == reservation.user_id).first()
        if user:
            LOAN_DAYS = {"student": 14, "teacher": 30, "visitor": 7}
            user_type = getattr(user, "type", "visitor")
            loan_days = LOAN_DAYS.get(user_type, 7)
            new_loan = Loan(
                user_id=user.id,
                book_id=book.id,
                start_date=date.today(),
                end_date=date.today() + timedelta(days=loan_days),
                returned=False,
                extended=False,
                status=LoanStatus.active
            )
            db.add(new_loan)
        reservation.status = "completed"
    else:
        book.stock_for_loan += 1

    db.commit()
    db.refresh(loan)
    # print(multa_msg)  # Puedes loguear el mensaje si quieres
    return loan

