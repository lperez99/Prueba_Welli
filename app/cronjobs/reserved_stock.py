import schedule
import time
from app.services import reserved_stock
from datetime import datetime, timedelta, UTC

def job():
    print("Procesando compras pendientes...")
    reserved_stock.process_pending_purchases()

schedule.every(1).minutes.do(job)

if __name__ == "__main__":
    print("Iniciando job de actualización de compras pendientes...")
    now = datetime.now(UTC)
    while True:
        schedule.run_pending()
        time.sleep(1)