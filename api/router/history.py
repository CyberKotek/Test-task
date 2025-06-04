import sys
sys.path.append("../")

from typing import List
from fastapi import APIRouter, Depends, HTTPException
import schemas, database, models
from sqlalchemy.orm import Session
import oauth2


router = APIRouter(
    tags=["History"],
    prefix="/history"
)


@router.get('/', response_model=List[schemas.ShowReturnedBorrow])
def get_all(db: Session = Depends(database.get_db), current_user: schemas.Librarian = Depends(oauth2.get_current_user)):
    return db.query(models.ReturnedBorrows).all()


@router.post("/find", response_model=List[schemas.ShowReturnedBorrow])
def find_all(request: schemas.FindReturnedBorrow, db: Session = Depends(database.get_db), current_user: schemas.Librarian = Depends(oauth2.get_current_user)):
    querry_dict = {}
    request_dict = request.dict()
    for i in request_dict:
        if (request_dict[i]):
            querry_dict[i] = request_dict[i]

    returned_borrows = db.query(models.ReturnedBorrows).filter_by(**querry_dict).all()
    if (not returned_borrows):
        raise HTTPException(status_code=404, detail=f"No such returned borrow")
    return returned_borrows