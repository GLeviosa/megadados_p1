from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import null
from fastapi import HTTPException, status

import models, schemas


def get_discipline(db: Session, discipline_id: int):
    return db.query(models.Discipline).filter(models.Discipline.id == discipline_id).first()


def get_discipline_by_name(db: Session, name: str):
    return db.query(models.Discipline).filter(models.Discipline.name == name).first()


def get_disciplines(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Discipline).offset(skip).limit(limit).all()


def create_discipline(db: Session, discipline: schemas.DisciplineCreate):
    db_discipline = models.Discipline(name=discipline.name, professor=discipline.professor, notes=discipline.notes)
    db.add(db_discipline)
    db.commit()
    db.refresh(db_discipline)
    return db_discipline

def get_notes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Note).offset(skip).limit(limit).all()

def get_notes_discipline(db: Session, discipline_id: int , skip: int = 0):
    return db.query(models.Note).filter(models.Note.discipline_id == discipline_id).offset(skip).all()

def create_discipline_note(db: Session, note: schemas.NoteCreate, discipline_id: int):
    db_note = models.Note(**note.dict(), discipline_id=discipline_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def update_discipline(db: Session, discipline_id: int, discipline: schemas.DisciplineCreate):
    discipline_to_update=db.query(models.Discipline).filter(models.Discipline.id==discipline_id).first()
    discipline_to_update.name=discipline.name
    discipline_to_update.professor=discipline.professor

    db.commit()

    print(discipline_to_update.name)
    print("-"*45)
    return discipline_to_update

def update_note(db: Session, note_id: int, note: schemas.NoteCreate):
    note_to_update=db.query(models.Note).filter(models.Note.id==note_id).first()
    note_to_update.description=note.description

    db.commit()
    return note_to_update

def delete_discipline(db: Session,  discipline: schemas.Discipline):
    discipline_to_delete=db.query(models.Discipline).filter(models.Discipline.id==discipline.id).first()
    notes = get_notes_discipline(db=db, discipline_id=discipline.id)
    for note in notes:
        db.delete(note)

    if discipline_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Resource Not Found")
    
    db.delete(discipline_to_delete)
    db.commit()
    
    return discipline_to_delete

def delete_note(db: Session,  note: schemas.Note, discipline: schemas.Discipline):
    note_to_delete=db.query(models.Note).filter(models.Note.discipline_id==discipline.id).first()

    if note_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Resource Not Found")
    db.delete(note_to_delete)
    db.commit()

    return note_to_delete