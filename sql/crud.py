from sqlalchemy.orm import Session
import functools

from sql import models
from sql.database import get_db


# Pas la peine de regarder ca

def use_db(func):
    """
    Wrapper creating a connection to the database and closing it after the function execution
    """
    @functools.wraps(func)
    def __use_db(*args, **kwargs):
        db = get_db()
        try:
            response = func(db, *args, **kwargs)
        finally:
            db.close()
        return response
    return __use_db


def authenticate_user(username: str, password: str):
    user = get_user_by_username(username)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user


@use_db
def delete_element_from_db(db: Session, element_to_delete):
    db.delete(element_to_delete)
    db.commit()
    return


# Le code commence ici 

@use_db
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


@use_db
def get_user_by_username(db, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


@use_db
def create_user(db, db_user):
    db.add(db_user)
    db.commit()
    return db_user


@use_db
def get_users(db: Session, skip: int = 0, limit: int = 50000):
    return db.query(models.User).offset(skip).all()


@use_db
def get_etude_by_id(db: Session, etude_id: int):
    return db.query(models.Etude).filter_by(id=etude_id).first()


@use_db
def get_nombre_etudes(db: Session):
    return db.query(models.Etude).filter_by(est_archivee=False).count()


@use_db
def get_etudes(db: Session, page: int =1, cards_per_page: int =30, est_archivee: bool =False):
    etudes = db.query(models.Etude).filter_by(est_archivee=est_archivee).all()
    page = 1 if page < 1 else page
    #borne inf: 0 so on est page 1, sinon 31, 61 etc
    borne_inf = 0 if page == 1 else 1 + (page - 1) * cards_per_page 
    # borne sup: 31, 61, ...
    borne_sup = 1 + page * cards_per_page
    etudes_paginees = etudes[borne_inf:borne_sup]
    return etudes_paginees