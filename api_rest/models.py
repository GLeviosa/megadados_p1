from database import Base
from sqlalchemy import String, Integer, Column, Text, ForeignKey
from typing import Optional, List
from sqlalchemy.orm import relation, relationship

class Discipline(Base):
    __tablename__ = 'disciplines'
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String(50), nullable=False,unique=True, index=True)
    professor = Column(String(50), index=True)
    notes = relationship("Note", back_populates="discip", cascade="all, delete-orphan")

class Note(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True, index=True)
    discipline_id = Column(Integer, ForeignKey("disciplines.id"))
    description = Column(String, index=True)
    discip = relationship("Discipline", back_populates="notes")