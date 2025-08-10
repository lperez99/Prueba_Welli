from app.database import SessionLocal
from app.models.purchase import Purchase, PurchaseStatus
from datetime import datetime, timedelta, UTC
import random
import time

def reserve_stock_for_pending_purchases():
    db = SessionLocal()
    now = datetime.now(UTC)
    pending_purchases = db.query(Purchase).filter(
        Purchase.status == PurchaseStatus.pending,
        Purchase.reserved_until == None
    ).all()
    for purchase in pending_purchases:
        purchase.reserved_until = now + timedelta(minutes=1)
        print(f"Reserva temporal de stock para compra {purchase.id} hasta {purchase.reserved_until}")
    db.commit()
    db.close()

def process_pending_purchases():
    db = SessionLocal()
    now = datetime.now(UTC)
    pending_purchases = db.query(Purchase).filter(
        Purchase.status == PurchaseStatus.pending,
        Purchase.reserved_until != None,
        Purchase.reserved_until <= now
    ).all()
    for purchase in pending_purchases:
        new_status = random.choice([PurchaseStatus.approved, PurchaseStatus.rejected])
        purchase.status = new_status
        if new_status == PurchaseStatus.rejected:
            # Solo suma stock si es compra física
            if purchase.type == "physical":
                purchase.book.stock_physical_for_sell += purchase.quantity
            print(f"Compra {purchase.id} RECHAZADA. Stock devuelto.")
        else:
            print(f"Compra {purchase.id} APROBADA. Stock descontado.")
    db.commit()
    db.close()

if __name__ == "__main__":
    print("Reservando stock por 1 minuto para compras pendientes...")
    reserve_stock_for_pending_purchases()

    print("Procesando compras pendientes cuyo tiempo de reserva expiró (primer chequeo)...")
    process_pending_purchases()

    # Revisa cada minuto durante 10 minutos adicionales
    for i in range(10):
        print(f"Esperando {i+1} minuto(s)...")
        time.sleep(60)
        print("Revisando nuevamente compras pendientes cuyo tiempo de reserva expiró...")
        process_pending_purchases()