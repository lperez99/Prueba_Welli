from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schema.purchase import PurchaseCreate, PurchaseOut
from app.services import purchase 
from app.models.purchase import Purchase

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=PurchaseOut)
def create_purchase_endpoint(purchase_in: PurchaseCreate, db: Session = Depends(get_db)):
    try:
        return purchase.create_purchase(db, purchase_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[PurchaseOut])
def list_purchases(db: Session = Depends(get_db)):
    return db.query(Purchase).all()