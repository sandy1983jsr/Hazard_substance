from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import date

class LocationBase(BaseModel):
    name: str
    country: str
    department: Optional[str]

class LocationCreate(LocationBase): pass

class Location(LocationBase):
    id: int
    class Config:
        orm_mode = True

class SubstanceBase(BaseModel):
    name: str
    cas_number: str
    supplier: Optional[str]
    hazard_class: Optional[str]
    regulatory_tags: Optional[Dict] = {}
    sds_path: Optional[str]
    sds_expiry: Optional[date]

class SubstanceCreate(SubstanceBase): pass

class Substance(SubstanceBase):
    id: int
    class Config:
        orm_mode = True

class SubstanceLocationBase(BaseModel):
    usage_context: Optional[str]
    quantity: Optional[str]
    remarks: Optional[str]

class SubstanceLocationCreate(SubstanceLocationBase):
    substance_id: int
    location_id: int

class SubstanceLocation(SubstanceLocationBase):
    id: int
    substance_id: int
    location_id: int
    class Config:
        orm_mode = True
