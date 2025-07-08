from sqlalchemy.orm import Session
from app import models, schemas

def create_substance(db: Session, substance: schemas.SubstanceCreate):
    db_sub = models.Substance(**substance.dict())
    db.add(db_sub)
    db.commit()
    db.refresh(db_sub)
    return db_sub

def get_substances(db: Session):
    return db.query(models.Substance).all()

def create_location(db: Session, location: schemas.LocationCreate):
    db_loc = models.Location(**location.dict())
    db.add(db_loc)
    db.commit()
    db.refresh(db_loc)
    return db_loc

def get_locations(db: Session):
    return db.query(models.Location).all()

def assign_substance_location(db: Session, sl: schemas.SubstanceLocationCreate):
    db_sl = models.SubstanceLocation(**sl.dict())
    db.add(db_sl)
    db.commit()
    db.refresh(db_sl)
    return db_sl

def update_substance_regulation(db: Session, substance_id, region, new_tag):
    sub = db.query(models.Substance).filter_by(id=substance_id).first()
    if sub:
        tags = sub.regulatory_tags or {}
        tags[region] = new_tag
        sub.regulatory_tags = tags
        db.commit()

def get_all_substances(db: Session):
    return db.query(models.Substance).all()

def compliance_summary(db: Session):
    subs = db.query(models.Substance).all()
    summary = {}
    for sub in subs:
        for reg, tag in (sub.regulatory_tags or {}).items():
            summary.setdefault(reg, {"at_risk": 0, "count": 0})
            summary[reg]["count"] += 1
            if tag.get("status") in ["Candidate", "Listed", "Active"]:
                summary[reg]["at_risk"] += 1
    return summary

def get_alerts(db: Session):
    from datetime import date, timedelta
    alerts = []
    subs = db.query(models.Substance).all()
    for sub in subs:
        if sub.regulatory_tags and (
            sub.regulatory_tags.get("REACH", {}).get("status") == "Candidate" or
            sub.regulatory_tags.get("Prop65", {}).get("status") == "Listed"
        ):
            alerts.append({
                "substance": sub.name,
                "cas": sub.cas_number,
                "alert": "Regulatory risk"
            })
        if sub.sds_expiry and (sub.sds_expiry - date.today()).days < 30:
            alerts.append({
                "substance": sub.name,
                "cas": sub.cas_number,
                "alert": f"SDS expires soon ({sub.sds_expiry})"
            })
    return alerts
