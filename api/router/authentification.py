import sys
sys.path.append("../")

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
import schemas, database, models
from sqlalchemy.orm import Session
from hashing import Hash
from JWTtoken import create_access_token

router = APIRouter(
    tags=["Login"],
    prefix="/login"
)

@router.post('/')
# def login(request: schemas.OauthForm, db: Session = Depends(database.get_db)):
#     librarian = db.query(models.Librarians).filter(models.Librarians.email == request.email).first()
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    librarian = db.query(models.Librarians).filter(models.Librarians.email == request.username).first()
    if (not librarian):
        raise HTTPException(status_code=400, detail=f"Incorrect username or password")

    if (not Hash.verify(librarian.password, request.password)):
        raise HTTPException(status_code=404, detail=f"Incorrect username or password")

    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": librarian.email})


    return {"access_token": access_token, "token_type": "bearer"}