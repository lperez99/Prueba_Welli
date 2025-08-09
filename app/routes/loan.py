from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schema.loan import LoanCreate, LoanOut
from app.services import loan
from app.database import SessionLocal
from app.services import reservation 

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=LoanOut)
def create_loan_endpoint(loan_in: LoanCreate, db: Session = Depends(get_db)):
    try:
        return loan.create_loan(db, loan_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{loan_id}/extend", response_model=LoanOut)
def extend_loan_endpoint(loan_id: int, db: Session = Depends(get_db)):
    try:
        return loan.extend_loan(db, loan_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/", response_model=list[LoanOut])
def list_loans(db: Session = Depends(get_db)):
    return loan.get_loans(db)

@router.put("/{loan_id}/return", response_model=LoanOut)
def return_loan_endpoint(loan_id: int, db: Session = Depends(get_db)):
    try:
        return loan.return_loan(db, loan_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

