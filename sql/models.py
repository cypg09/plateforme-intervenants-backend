from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from passlib.context import CryptContext
from datetime import datetime

from sql.database import Base, get_db


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Documentation about tables links with SQLAlchemy ORM : https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html


def get_password_hash(password):
    return pwd_context.hash(password)


# Dans l'ordre :
# 1. Creer le BA
# 2. Creer l'User
# 3. Creer l'Intervenant ou le RH
# 
# Les arguments qui sont entre Mandatory args: et End sont OBLIGATOIRES pour créer l'objet


class BA(Base):
    __tablename__ = "ba"

    id = Column(Integer, primary_key=True, index=True)
    # Mandatory args:
    adresse = Column(String(256), nullable=False)
    ville_de_naissance = Column(String(256), nullable=False)
    carte_vitale_pdf_path = Column(String(256), nullable=False)
    carte_etudiant_pdf_path = Column(String(256), nullable=False)
    piece_identite_pdf_path = Column(String(256), nullable=False)
    photo_jpeg_path = Column(String(256), nullable=False)
    rib_pdf_path = Column(String(256), nullable=False)
    # End

    # One-to-One relationship with User
    user = relationship("User", back_populates="ba", uselist=False, lazy='select')


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    # Mandatory args
    username = Column(String(256), unique=True, index=True, nullable=False)

    #notation = Column(Float) #TODO a migrer dans RH

    prenom = Column(String(256))
    nom_de_famille = Column(String(256))

    campus = Column(String(256))
    promo = Column(String(256))

    # Cela signifie qu'il faut donner en argument l'id du bulletin d'adhesion pour creer un User
    ba_id = Column(Integer, ForeignKey('ba.id')) 

    # End

    hashed_password = Column(String(256))
    account_creation_date = Column(DateTime, default=datetime.utcnow())
    ba_est_complet = Column(Boolean, default=False) #TODO

    # Relationships
    ## One to one relationship between User and BA:
    ba = relationship("BA", back_populates="user", lazy='select')
    ## One to one relationship between User and Intervenant:
    intervenant = relationship("Intervenant", back_populates="user", useList=False, lazy='subquery')

    def verify_password(self, plain_password):
        password_is_correct = pwd_context.verify(plain_password, self.hashed_password)
        return password_is_correct

    def create_password(self, plain_password): 
        self.hashed_password = get_password_hash(plain_password)
        return True
    
    def marquer_ba_complet(self):
        self.ba_est_complet = True
        return


class Intervenant(Base):
    __tablename__ = "intervenant"

    id = Column(Integer, primary_key=True, index=True)
    # Mandatory args :

    # Cela signifie qu'il faut donner en argument l'id du User pour creer un Intervenant
    user_id = Column(Integer, ForeignKey('user.id'))
    # End

    etudes_realisees = relationship("Etudes")
    etudes_postulees = relationship("Etudes")
    est_premium = Column(Boolean, default=False)

    ## One to one relationship between User and Intervenant:
    user = relationship("User", back_populates="intervenant", lazy='joined')


    def mettre_premium(self, premium_nouvel_etat: bool =True) -> bool:
        """
        Fonction qui toggle l'etat du premium : permet de marquer un intervenant "intervenant premium" ou la reciproque. 

        :param premium_nouvel_etat: nouvel etat de la variable "est_premium":
            True si on veut que le consultant devienne premium,
            False si on veut qu'il ne le soit plus.
            defaults to True
        :type premium_nouvel_etat: bool, optional
        """
        self.est_premium = premium_nouvel_etat
        return self.est_premium

    # One-to-one relationship with User
    user = relationship("User", back_populates="intervenant")


class Etude(Base):
    __tablename__ = "etude"

    id = Column(Integer, primary_key=True, index=True)
    type_de_phase = Column(String(256), nullable=False)
    remuneration = Column(Float, nullable=False)
    date_signature = Column(DateTime, nullable=False)
    date_debut = Column(Datetime, nullable=False)
    date_fin = Column(Datetime, nullable=False)
    incrementation = Column(String(256), nullable=False)
    lien_beequick = Column(String(256), nullable=False)
    nombre_max_candidats = Column(Integer, nullable=False)
    est_archivee = Column(Boolean, default=False)

    candidats = relationship("Intervenant") #TODO
    intervenants = relationship("Intervenant") #TODO

    def archiver_etude(self):
        self.est_archivee = True
        return


