from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from .config import settings

from . import schemas, models, database

# Define an instance of OAuth2PasswordBearer with a token URL of 'login'.
oath2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# Define constants for the secret key, algorithm, and access token expiration time.
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# Function to CREATE a JWT ACCESS TOKEN with an expiration time of 30 minutes.
def create_access_token(data: dict):
    # Make a copy of the input data dictionary.
    to_encode = data.copy()
    # Set the token expiration time to 30 minutes from the current time.
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Add the token expiration time to the data dictionary.
    to_encode.update({'exp': expire})
    # Encode the data dictionary as a JWT token using the secret key and algorithm.
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    # Return the encoded JWT token.
    return encoded_jwt

# Function to verify a JWT access token and return a TokenData object with the user ID.
def verify_access_token(token: str, credentials_exception):
    try:
        # Decode the JWT access token using the secret key and algorithm.
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        # Extract the user ID from the decoded payload.
        id: str = payload.get("user_id")
        # If there is no user ID in the payload, raise a credentials exception.
        if id is None:
            raise credentials_exception
        # Create a TokenData object with the user ID.
        token_data = schemas.TokenData(id=id)
    except JWTError:
        # If there is an error decoding the JWT token, raise a credentials exception.
        raise credentials_exception
    # Return the TokenData object with the user ID.
    return token_data

# Function to get the current user's ID from an OAuth2 access token.
def get_current_user(token: str = Depends(oath2_scheme), 
                     db:Session=Depends(database.get_db)):
    # Create an HTTPException object to raise if the credentials are invalid.
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail='Could not validate credentials',
                                          headers={"WWW-Authenticate": "Bearer"})
    token=verify_access_token(token, credentials_exception)
    user=db.query(models.User).filter(models.User.id==token.id).first()
    # Verify the access token and get the user ID using the verify_access_token function.
    return user
