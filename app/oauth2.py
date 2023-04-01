from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from . import schemas
oath2_scheme=OAuth2PasswordBearer(tokenUrl='login')
# SECRET KEY
# ALGORITHM
# EXPIRATION TIME

SECRET_KEY = 'FGNOGBNAWECADFASR9482-JRVGWT404V3'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now()+timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode,   SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)
        id: str = payload.get("users_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token: str=Depends(oath2_scheme)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Could not validate credentials', headers={"WWW-Authenticate":"Bearer"})
    return verify_access_token(token, credentials_exception)