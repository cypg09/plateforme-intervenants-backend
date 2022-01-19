from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from passlib.context import CryptContext
from datetime import datetime

from sql.database import Base, get_db


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def get_password_hash(password):
    return pwd_context.hash(password)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(256), unique=True, index=True)
    est_rh = Column(Boolean, nullable=False)
    notation = Column(Float)
    ba_id = relationship("BA") #TODO
    prenom = Column(String(256))
    nom_de_famille = Column(String(256))
    campus = Column(String(256))
    promo = Column(String(256))
    etudes_realisees = relationship("Etudes") #TODO
    etudes_postulees = relationship("Etudes") #TODO

    hashed_password = Column(String(256))
    account_creation_date = Column(DateTime, default=datetime.utcnow())
    ba_est_complet = Column(Boolean, default=False) #TODO
    est_premium = Column(Boolean, defautl=False) #TODO

    def verify_password(self, plain_password):
        password_is_correct = pwd_context.verify(plain_password, self.hashed_password)
        return password_is_correct

    def create_password(self, plain_password): 
        self.hashed_password = get_password_hash(plain_password)
        return True
    
    def marquer_ba_complet(self):
        self.ba_est_complet = True
        return

    def mettre_premium(self):
        self.ba_est_complet = True
        return


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

    candidats = relationship("User") #TODO

    def archiver_etude(self):
        self.est_archivee = True
        return


class BA(Base):
    __tablename__ = "ba"

    id = Column(Integer, primary_key=True, index=True)

    adresse = Column(String(256), nullable=False)
    ville_de_naissance = Column(String(256), nullable=False)
    carte_vitale_pdf_path = Column(String(256), nullable=False)
    carte_etudiant_pdf_path = Column(String(256), nullable=False)
    piece_identite_pdf_path = Column(String(256), nullable=False)
    photo_jpeg_path = Column(String(256), nullable=False)
    rib_pdf_path = Column(String(256), nullable=False)

    user = relationship("User") #TODO
