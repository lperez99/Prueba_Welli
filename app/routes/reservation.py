from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.reservation import Reservation
from app.schema.reservation import ReservationCreate, ReservationOut
from app.crud import reservation as reservation_crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[ReservationOut])
def list_reservations(db: Session = Depends(get_db)):
    return db.query(Reservation).all()

@router.post("/", response_model=ReservationOut)
def create_reservation(reservation_in: ReservationCreate, db: Session = Depends(get_db)):
    return reservation_crud.create_reservation(db, reservation_in)

@router.delete("/{reservation_id}/canceled", response_model=dict)
def confirmed_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    reservation.status = "cancelled"  # O StatusReservation.cancelled si usas Enum
    db.commit()
    return {"detail": "Reserva cancelada"}

