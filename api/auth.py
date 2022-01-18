from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta

from sql import crud
from sql import models
from sql.database import get_db

SECRET_KEY = "3543c13ef03604b69a6c1d552c7cdab69cb8c4254ae44e0bc89933f089a67f13"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

api_auth = APIRouter(
    prefix="/auth"
)

token_auth = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: int =30):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_username(username)
    if not user:
        raise credentials_exception
    return {"username": user.username, "token": token}


@token_auth.post(path="/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return {"access_token": access_token, "token_type": "bearer"}


@api_auth.post("/register")
def register(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    db_user = crud.get_user_by_username(username)
    if db_user:
        raise HTTPException(
            status_code=300,
            detail="Username already exists",
            headers={"WWW-Authenticate": "Bearer"},
            )
    db_user = models.User(
        username=username
    )
    db_user.create_password(password)
    db_user = crud.create_user(db_user)
    return db_user


@api_auth.get("/users/me/")
def read_users_me(token: OAuth2PasswordBearer = Depends(oauth2_scheme)):
    return get_current_user(token)

