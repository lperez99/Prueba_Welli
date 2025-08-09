from app.models.reservation import Reservation
from sqlalchemy.orm import Session

def create_reservation(db: Session, reservation_in):

    reservation = Reservation(**reservation_in.dict())
    db.add(reservation)
    db.commit()
    db.refresh(reservation)
    return reservation