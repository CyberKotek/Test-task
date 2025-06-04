import sys
sys.path.append("../")

from fastapi import APIRouter, Depends, HTTPException
import schemas, database, models
from sqlalchemy.orm import Session
from hashing import Hash



router = APIRouter(
    tags=["Registration"],
    prefix="/register"
)


@router.post('/')
async def create_librarian(request: schemas.Librarian, db: Session = Depends(database.get_db)):
    existing = db.query(models.Librarians).filter(models.Librarians.email == request.email).first()
    if (existing):
        raise HTTPException(status_code=400, detail=f"Librarian with such email already exists")

    new_librarian = models.Librarians(email=request.email, name=request.name, password=Hash.get_hash(request.password))
    db.add(new_librarian)
    db.commit()
    db.refresh(new_librarian)
    return new_librarian