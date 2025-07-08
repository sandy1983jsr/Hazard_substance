from celery import Celery
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.regulations import update_reach, update_prop65, update_tsca, update_india

celery = Celery(__name__, broker='redis://localhost:6379/0')

@celery.task
def update_all_regulations():
    db: Session = SessionLocal()
    try:
        update_reach(db)
        update_prop65(db)
        update_tsca(db)
        update_india(db)
    finally:
        db.close()
