from sqlalchemy.orm import Session
import functools 

from . import models, schemas
from sql.database import get_db


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
def update_user_current_capital(db: Session, username, current_capital: float):
    user = get_user_by_username(username)
    if not user:
        return False
    user.current_capital = current_capital
    db.add(user)
    db.commit()
    return True

def get_user_current_capital(username):
    user = get_user_by_username(username)
    if not user:
        return False
    return user.current_capital


@use_db
def get_currencies(db: Session):
    return db.query(models.Symbol).all()


@use_db
def create_currency(db: Session, name):
    currency = models.Currency(name=name)
    db.add(currency)
    db.commit
    return currency


@use_db
def get_currency(db: Session, name):
    currency = db.query(models.Currency).filter_by(name=name).first()
    if not currency:
        currency = create_currency(name)
    return currency


@use_db
def create_symbol(db: Session, db_symbol):
    db.add(db_symbol)
    db.commit()
    return db_symbol


@use_db
def create_value(db: Session, db_value):
    db.add(db_value)
    db.commit()
    return db_value


@use_db
def get_value_by_symbol(db: Session, symbol: str):
    return db.query(models.SymbolValue).filter_by(symbol_symbol=symbol).first()


@use_db
def get_value_by_id(db: Session, value_id: int):
    return db.query(models.SymbolValue).filter_by(id=value_id).first()


@use_db
def set_api(db: Session, username, api_key, api_secret):
    user = get_user_by_username(username)
    if not user:
        return False
    user.set_api(api_key, api_secret)
    db.add(user)
    db.commit()
    return True


@use_db 
def get_user_assets(db: Session, username):
    user = get_user_by_username(username)
    if not user:
        return list()
    return list(db.query(models.UserAsset).filter(models.UserAsset.user_id == user.id).all())


@use_db
def add_user_asset(db: Session, username, currency, total_balance):
    print("adding user asset")
    user = get_user_by_username(username)
    if not user:
        print("no user")
        return False
    #user_assets = get_user_assets(username)
    #print(user_assets)
    #return
    #if not None in user_assets and user_assets is not None:
    #    user_assets_currencies = [user_asset.base.name for user_asset in user_assets]
    #if currency in user_assets_currencies:
    #    #symbol = db.query(models.Currency).filter()
    #    user_asset = db.query(models.UserAsset).filter(models.UserAsset.base.name == currency).filter(models.UserAsset.user_id == user.id).first()
    #    user_asset.quantity = total_balance
    #else:
    #    currency_object = db.query(models.Currency).filter(models.Currency.name == currency).first()
    #    user_asset = models.UserAsset(
    #        base=currency_object,
    #        user=user,
    #        quantity=total_balance
    #        )

    currency_object = db.query(models.Currency).filter(models.Currency.name == currency).first()
    if not currency_object:
        currency_object = models.Currency(name=currency)
        db.add(currency_object)
        db.commit()
    user_asset = models.UserAsset(
        currency=currency_object,
        user=user,
        quantity=total_balance
        )
    db.add(user_asset)
    db.commit()
    print(f"{currency} : {total_balance}, {user_asset.id}")
    return True
