from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Lien qui permet de connecter l'environnement à la base de données mysql
DATABASE_URL = "mysql+mysqlconnector://root:test@localhost/result_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
