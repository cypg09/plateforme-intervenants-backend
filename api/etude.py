from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import create_engine

from sql import crud
from api.auth import oauth2_scheme, get_current_user


api_etude = APIRouter(
    prefix="/etude"
)

@api_etude.get("/nombreEtudes")
def get_nombre_etudes():
    nombre = crud.get_nombre_etudes()
    return {
        "nombreEtudes": nombre
    }
