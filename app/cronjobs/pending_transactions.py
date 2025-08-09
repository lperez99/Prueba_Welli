import schedule
import time
from app.services.pending_transactions import process_loan_fines
from app.models.user import User
from app.models.book import Book
from app.models.loan import Loan
from app.models.reservation import Reservation
from app.models.purchase import Purchase

def job():
    print("Procesando multas de prestamos activos...")
    process_loan_fines()

schedule.every().day.at("01:00").do(job)  # Corre todos los días a la 1 AM

if __name__ == "__main__":
    print("Ejecutando job de multas de prestamos manualmente...")
    job()