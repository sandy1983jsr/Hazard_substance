from sqlalchemy import Column, Integer, String, ForeignKey, Date, JSON, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    department = Column(String, nullable=True)
    substances = relationship("SubstanceLocation", back_populates="location")

class Substance(Base):
    __tablename__ = 'substances'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    cas_number = Column(String, nullable=False, unique=True)
    supplier = Column(String, nullable=True)
    hazard_class = Column(String, nullable=True)
    regulatory_tags = Column(JSON, default={})  # {"REACH": {...}, "Prop65": {...}, ...}
    sds_path = Column(String, nullable=True)
    sds_expiry = Column(Date, nullable=True)
    locations = relationship("SubstanceLocation", back_populates="substance")

class SubstanceLocation(Base):
    __tablename__ = 'substance_locations'
    id = Column(Integer, primary_key=True)
    substance_id = Column(Integer, ForeignKey('substances.id'))
    location_id = Column(Integer, ForeignKey('locations.id'))
    usage_context = Column(String)
    quantity = Column(String)
    remarks = Column(String)
    substance = relationship("Substance", back_populates="locations")
    location = relationship("Location", back_populates="substances")
