from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, models, oauth2, schemas, utils

# Create a router for authentication endpoints with a tag for OpenAPI documentation
router = APIRouter(tags=['Authentication'])

# Create a route for user login that expects an OAuth2 password request form and a database session
@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # Get the user with the given email from the database
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()
    # If the user doesn't exist, raise an HTTP 403 error with an appropriate message
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials')

    # If the password is incorrect, raise an HTTP 403 error with an appropriate message
    if not utils.verify(user_credentials.password, user.password):
        print('doesnt working')
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, details='Invalid credentials')

    # Create an access token for the user and return it with its token type
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {'access_token': access_token, "token_type": "bearer"}
