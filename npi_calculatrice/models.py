from sqlalchemy import Column, Float, Integer, String
from database import Base

class CalculResult(Base):
    # Défini la table dans la base de données
    __tablename__ = "calcul_results"

    # Contenu du tableau dans la bdd
    id = Column(Integer, primary_key=True, index=True)
    operation = Column(String, index=True)
    result = Column(Float)


    # convertir l'objet en un dictionaire
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Operation(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, index=True)
    expression = Column(String(255), nullable=False)
    result = Column(Float, nullable=False)


