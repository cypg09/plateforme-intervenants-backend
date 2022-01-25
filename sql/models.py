from sqlalchemy import Table, Boolean, Column, ForeignKey, Integer, String, DateTime, Float
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

# Association tables for many-to-many links : cf https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#many-to-many
etudes_postulees_x_intervenants = Table('etudes_postulees_x_intervenants', Base.metadata,
    Column('etudes_postulees_id', ForeignKey('etude.id')),
    Column('intervenant_id', ForeignKey('intervenant.id'))
)

etudes_realisees_x_intervenants = Table('etudes_realisees_x_intervenants', Base.metadata,
    Column('etudes_realisees_id', ForeignKey('etude.id')),
    Column('intervenant_id', ForeignKey('intervenant.id'))
)

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

    # Relationships
    ## One-to-One relationship with User
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
    intervenant = relationship("Intervenant", back_populates="user", uselist=False, lazy='subquery')

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

    est_premium = Column(Boolean, default=False)

    # Relationships
    ## One to one relationship between User and Intervenant:
    user = relationship("User", back_populates="intervenant", lazy='joined')
    ## Many to many relationship between Etude et Intervenant: 
    etudes_postulees = relationship(
        "Etude",
        secondary=etudes_postulees_x_intervenants,
        back_populates="candidats"
    )
    etudes_realisees = relationship(
        "Etude", 
        secondary=etudes_realisees_x_intervenants,
        back_populates="intervenants"
    )

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
    # Mandatory args :
    date_signature = Column(DateTime, nullable=False)
    date_debut = Column(DateTime, nullable=False)
    date_fin = Column(DateTime, nullable=False)
    incrementation = Column(String(256), nullable=False)
    nom_du_client = Column(String(256), nullable=False)
    lien_beequick = Column(String(256), nullable=False)
    nombre_max_candidats = Column(Integer, nullable=False)
    #phases TODO
    # End

    est_archivee = Column(Boolean, default=False)

   

    def archiver_etude(self, nouvel_etat_archivage: bool =True) -> bool:
        """
        Fonction qui toggle l'etat d'archivage : permet de marquer une etude archivee ou reciproque.

        :param nouvel_etat_archivage: nouvel etat de la variable "est_archivee":
            True si on veut que l'etude soit archivee,
            False si on veut qu'elle ne le soit plus.
            defaults to True
        :type nouvel_etat_archivage: bool, optional
        """
        self.est_archivee = nouvel_etat_archivage
        return self.est_archivee
    
    def get_nombre_candidats_premium():
        # TODO
        return

class Phase(Base):
    __tablename__="phase"
    type_de_phase = Column(String(256), nullable=False)
    date_debut = Column(DateTime, nullable=False)
    date_fin = Column(DateTime, nullabe=False)
    # Relationships
    ## Many to many relationship between Etude et Intervenant: 
    candidats = relationship(
        "Intervenant",
        secondary=etudes_postulees_x_intervenants,
        back_populates="etudes_postulees"
    )
    intervenants = relationship(
        "Intervenant", 
        secondary=etudes_realisees_x_intervenants,
        back_populates="etudes_realisees"
    )
    remuneration = Column(Float, nullable=False)
    campus = Column(String(32), nullabe=False)
    description = Column(String, nullable=False)