from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import models
from models import CalculResult
from database import Base, engine, SessionLocal
from fastapi.responses import StreamingResponse
import uvicorn
import pandas as pd
import io
import logging

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

operations = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a / b,
}

#fonction qui permet d'évaluer une expression mathématique en NPI.
def npi_calculatrice(expression):
    stack = []

    for token in expression.split():
        if token in operations:
            b = stack.pop()
            a = stack.pop()
            stack.append(operations[token](a, b))
        else:
            stack.append(float(token))

    return stack.pop()

def save_calculation_to_db(db: Session, expression: str, result: float) -> models.CalculResult:
    try:
        db_calculation = models.CalculResult(operation=expression, result=result)
        db.add(db_calculation)
        db.commit()
        db.refresh(db_calculation)
        return db_calculation
    except Exception as e:
        db.rollback()
        raise e


def display_and_save_calculation(expression: str, result: float, db: Session):
    print(f"Expression: {expression}, Resultat: {result}")
    saved_calculation = save_calculation_to_db(db, expression, result)
    print(f"Calcul enregistré avec l'ID: {saved_calculation.id}")

 #API route pour récuperer les datas sur le fichier csv
@app.get("/export_csv")
async def export_csv(db: Session = Depends(get_db)):
    calculations = db.query(models.CalculResult).all()
    df = pd.DataFrame([calculation.as_dict() for calculation in calculations])

    # Elle écrit le DataFrame dans un objet BytesIO
    csv_file = io.BytesIO()
    df.to_csv(csv_file, index=False)
    csv_file.seek(0)

    # Créer une réponse de streaming pour le téléchargement
    response = StreamingResponse(iter([csv_file.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=calculations.csv"

    return response

#EndPoints Get qui affiche toutes les opérations enregistrer sur la bdd
@app.get("/calculations")
async def get_calculations(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    calculations = db.query(models.CalculResult).offset(skip).limit(limit).all()
    return {"calculations": calculations}

#EndPoints Post qui permet de poster toutes les opérations afin qu'elle puisse être enregistrer sur la bdd
@app.post("/calculate")
async def calculate(expression: str, db: Session = Depends(get_db)):
    try:
        result = npi_calculatrice(expression)
        display_and_save_calculation(expression, result, db)
        return {"result": result}
    except (ValueError, ZeroDivisionError, IndexError) as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")


def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8000)

#requête principal qui lance le serveur ainsi que la calculatrice
def main():
    run_server()

    while True:
        expression = input("Entrez une expression en NPI (ou 'exit' pour quitter) : ")

        if expression.lower() == 'exit':
            print("Au revoir!")
            break

        try:
            result = npi_calculatrice(expression)
            display_and_save_calculation(expression, result, db=SessionLocal())
        except (ValueError, ZeroDivisionError, IndexError) as e:
            print(f"Erreur : {str(e)}")

if __name__ == "__main__":
    main()



