from fastapi import FastAPI, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import SessionLocal, engine
from datetime import date
import os

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/substances/", response_model=schemas.Substance)
def create_substance(substance: schemas.SubstanceCreate, db: Session = Depends(get_db)):
    return crud.create_substance(db=db, substance=substance)

@app.get("/substances/", response_model=list[schemas.Substance])
def list_substances(db: Session = Depends(get_db)):
    return crud.get_substances(db)

@app.post("/locations/", response_model=schemas.Location)
def create_location(location: schemas.LocationCreate, db: Session = Depends(get_db)):
    return crud.create_location(db=db, location=location)

@app.get("/locations/", response_model=list[schemas.Location])
def list_locations(db: Session = Depends(get_db)):
    return crud.get_locations(db)

@app.post("/substance-locations/", response_model=schemas.SubstanceLocation)
def assign_substance_location(sl: schemas.SubstanceLocationCreate, db: Session = Depends(get_db)):
    return crud.assign_substance_location(db, sl)

@app.post("/sds/upload/{substance_id}")
async def upload_sds(substance_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    folder = "sds_storage"
    os.makedirs(folder, exist_ok=True)
    filename = f"{substance_id}_{file.filename}"
    file_path = os.path.join(folder, filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    sub = db.query(models.Substance).filter_by(id=substance_id).first()
    if sub:
        sub.sds_path = file_path
        sub.sds_expiry = date.today().replace(year=date.today().year + 1)
        db.commit()
        db.refresh(sub)
    return {"status": "ok"}

@app.get("/dashboard/compliance")
def compliance_dashboard(db: Session = Depends(get_db)):
    return crud.compliance_summary(db)

@app.get("/dashboard/alerts")
def alerts_dashboard(db: Session = Depends(get_db)):
    return crud.get_alerts(db)
