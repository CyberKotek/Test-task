import sys
sys.path.append("../")

from typing import List
from fastapi import APIRouter, Depends
import schemas, database, models
from sqlalchemy.orm import Session
import oauth2


router = APIRouter(
    tags=["Librarians"],
    prefix="/librarians"
)


@router.get('/', response_model=List[schemas.ShowLibrarian])
async def create_librarian(db: Session = Depends(database.get_db), current_user: schemas.Librarian = Depends(oauth2.get_current_user)):
    result = db.query(models.Librarians).all()
    return result


@router.get('/{id}', response_model=schemas.ShowLibrarian)
async def create_librarian(id: int, db: Session = Depends(database.get_db), current_user: schemas.Librarian = Depends(oauth2.get_current_user)):
    result = db.query(models.Librarians).filter(models.Librarians.id == id).first()
    return result