import sys
sys.path.append("../utils")

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
import schemas, database, models, oauth2
from sqlalchemy.orm import Session


router = APIRouter(
    tags=["Readers"],
    prefix="/readers"
)


@router.get('/', response_model=List[schemas.ShowOnlyReader])
async def get_reader(db: Session = Depends(database.get_db), current_user: schemas.Librarian = Depends(oauth2.get_current_user)):
    readers = db.query(models.Readers).all()
    return readers


@router.post("/find")
def find_all(request: schemas.FindReader, db: Session = Depends(database.get_db), current_user: schemas.Librarian = Depends(oauth2.get_current_user)):
    querry_dict = {}
    request_dict = request.dict()
    for i in request_dict:
        if (request_dict[i]):
            querry_dict[i] = request_dict[i]

    readers = db.query(models.Readers).filter_by(**querry_dict).all()
    if (not readers):
        raise HTTPException(status_code=404, detail=f"No such readers")
    return readers


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_reader (request: schemas.Reader, db: Session = Depends(database.get_db), current_user: schemas.Librarian = Depends(oauth2.get_current_user)):
    existing = db.query(models.Readers).filter(models.Readers.email == request.email).first()
    if (existing):
        raise HTTPException(status_code=400, detail=f"Reader with such email already exists")

    new_reader = models.Readers(request)
    db.add(new_reader)
    db.commit()
    db.refresh(new_reader)
    return new_reader

@router.delete("/detele", status_code=status.HTTP_204_NO_CONTENT)
def delete_reader(id: int, db: Session = Depends(database.get_db), current_user : schemas.Librarian = Depends(oauth2.get_current_user)):
    reader = db.query(models.Readers).filter(models.Readers.id == id).first()
    if (not reader):
        raise HTTPException(status_code=400, detail=f"No reader with such ID")
    db.delete(reader)
    db.commit()
    return 0

@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def update_reader(request: schemas.Reader, id: int, db: Session = Depends(database.get_db), current_user : schemas.Librarian = Depends(oauth2.get_current_user)):
    reader = db.query(models.Readers).filter(models.Readers.id == id)
    if (not reader.first()):
        raise HTTPException(status_code=400, detail=f"No reader with such ID")
    reader.update(request.dict())
    db.commit()
    return 0