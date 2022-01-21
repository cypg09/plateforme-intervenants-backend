from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import create_engine

from sql import crud
from api.auth import oauth2_scheme, get_current_user


api_etude = APIRouter(
    prefix="/user"
)

