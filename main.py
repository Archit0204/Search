from fastapi import FastAPI, Depends, status, Response, HTTPException
import schemas, models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/add")
def addMedicine(request: schemas.Medicine, db: Session = Depends(get_db)):
    newMed = models.Medicine(name = request.name, salt = request.salt, symptom = request.symptom)
    db.add(newMed)
    db.commit()
    db.refresh(newMed)
    return newMed

@app.get("/name/{Name}",status_code = status.HTTP_200_OK, response_model = list[schemas.Medicine])
def fetchByName(Name: str, db: Session = Depends(get_db)):
    medicine = db.query(models.Medicine).filter(models.Medicine.name == Name).all()
    if not medicine:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Medicine with name - {Name} not found")
    return medicine

@app.get("/salt/{Salt}", status_code = status.HTTP_200_OK, response_model = list[schemas.Medicine])
def fetchBySalt(Salt :str , db: Session = Depends(get_db)):
    medicine = db.query(models.Medicine).filter(models.Medicine.salt == Salt).all()
    if not medicine:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Medicine with salt - {Salt} not found")
    return medicine

@app.get("/symptom/{Symptom}", status_code = status.HTTP_200_OK, response_model = list[schemas.Medicine])
def fetchBySymptom(Symptom: str, db: Session = Depends(get_db)):
    medicine = db.query(models.Medicine).filter(models.Medicine.symptom == Symptom).all()
    if not medicine:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Medicine with symptom - {Symptom} not found")
    return medicine
