from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import create_engine

from sql import crud
from api.auth import oauth2_scheme, get_current_user


api_rh = APIRouter(
    prefix="/rh"
)

@api_etude.get("/nombreEtudes")
def get_nombre_etudes():
    nombre = crud.get_nombre_etudes()
    return {
        "nombreEtudes": nombre
    }

@api_etude.get("/etudes")
def get_cards(page: int =1, cards_per_page: int =30):
    """
    Fonction qui récupère les études non-archivées et rend parmi ces études les numéros from_id jusqu'à to_id
    Exemple de l'implementation dans crud.py: 
    etudes_non_archivees = db.query(.....).filter_by(est_archivee=False).all()
    etudes = etudes_non_archivees[from_id:to_id+1]

    :param from_id: premiere id de l'étude récupérée parmi les etudes non archivees, defaults to 1
    :type from_id: int, optional
    :param to_id: derniere etude recuperee, defaults to 30
    :type to_id: int, optional
    """
    etudes = crud.get_etudes_non_archivees(page, cards_per_page)
    return [
        {
        "incrementation": etude.incrementation,
        "nomDuClient": etude.nom_du_client, 
        "type": etude.type_de_phase,
        "remuneration": etude.remuneration,
        "dateDeSignature": etude.date_signature,
        "nombreDePostulants": len(etude.candidats),
        "nombreDePostulantsPremium": etude.get_nombre_candidats_premium()
        } for etude in etudes]