from app.database import SessionLocal
from app.models.loan import Loan, LoanStatus
from app.models.user import User
from datetime import date

def process_loan_fines():
    db = SessionLocal()
    today = date.today()
    loans = db.query(Loan).filter(Loan.status == LoanStatus.active).all()
    for loan in loans:
        if loan.end_date and today > loan.end_date:
            days_late = (today - loan.end_date).days
            days_to_fine = days_late - (loan.days_fined or 0)
            if days_to_fine > 0:
                if days_late <= 30:
                    fine = days_to_fine * 2000
                else:
                    # Multa para días antes y después de 30
                    if loan.days_fined < 30:
                        fine = (min(days_late, 30) - loan.days_fined) * 2000 + (days_late - max(loan.days_fined, 30)) * 4000
                    else:
                        fine = days_to_fine * 4000
                user = db.query(User).filter(User.id == loan.user_id).first()
                if user:
                    user.fines += fine
                    print(f"Multa aplicada a {user.name}: ${fine:,.0f} por {days_to_fine} días nuevos de retraso en préstamo.")
                loan.days_fined = days_late
    db.commit()
    db.close()