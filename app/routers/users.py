from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas, utils
from ..database import get_db

router = APIRouter()  # Creating a FastAPI instance called router


# CREATE NEW USER
@router.post('/users', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    existing_user = db.query(models.User).filter(
        models.User.email == user.email).first()
    if existing_user:
        return existing_user
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# GET USER BY ID
@router.get('/users/{id}', status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Oops!💔💔💔💔💔💔 Looks like the user with ID {id} you're looking for isn't here. 😞🕵️‍♀️🔍😞")
    return user

# GET ALL USERS INFO
@router.get('/admin/usersinfo', status_code=status.HTTP_200_OK, response_model=List[schemas.UserOut])
def user_info(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

# UPDATE USER INFO
@router.put('/users/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.UserOut)
def update_user(id: int, updated_user: schemas.UserCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == str(id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Oops!💔💔💔💔💔💔 Looks like the user with ID {id} you're looking for isn't here. 😞🕵️‍♀️🔍😞")

    user.email = updated_user.email
    user.password = updated_user.password
    user.first_name = updated_user.first_name
    user.last_name = updated_user.last_name
    db.commit()  # make changes to DB
    db.refresh(user)  # return updated post to user
    return user
