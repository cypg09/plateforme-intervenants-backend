from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import create_engine

from sql import crud
from api.auth import oauth2_scheme, get_current_user


api_user = APIRouter(
    prefix="/user"
)


@api_user.get("/username")
def get_username(username):
    user = crud.get_user_by_username(username)
    return {
        "username": user.username
    }

@api_user.get("/etude/{etude_id}")
def get_etude_by_id(etude_id: int):
    etude = crud.get_etude_by_id(etude_id)
    if not etude:
        return {"id": 255}
    return {
        "etudeId": etude.id,
        "typeDePhase": etude.type_de_phase,
        "remuneration": etude.remuneration,
        "dateSignature": etude.date_signature,
    }
