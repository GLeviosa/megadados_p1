from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# GET_db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#GET all Disciplines
@app.get("/disciplines/",response_model=List[schemas.Discipline])
def read_disciplines(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    disciplines = crud.get_disciplines(db, skip=skip, limit=limit)
    return disciplines

#GET Discipline by ID
@app.get("/disciplines/{discipline_id}",response_model=schemas.Discipline)
def read_discipline(discipline_id: int, db: Session = Depends(get_db)):
    db_discipline = crud.get_discipline(db, discipline_id=discipline_id)
    if db_discipline is None:
        raise HTTPException(status_code=404, detail="Discipline not found")
    return db_discipline

#CREATE Discipline
@app.post("/disciplines/")
def create_discipline(discipline: schemas.DisciplineCreate, db: Session = Depends(get_db)):
    db_discipline = crud.get_discipline_by_name(db, name=discipline.name)
    if db_discipline:
        raise HTTPException(status_code=400, detail="Discipline already registered")
    return crud.create_discipline(db=db, discipline=discipline)

#ATT Discipline
@app.patch("/disciplines/{discipline_id}")
def update_discipline(discipline_id: int, discipline:schemas.DisciplineCreate, db: Session = Depends(get_db)):
    
    db_discipline = crud.get_discipline(db, discipline_id=discipline_id)
    if db_discipline:
        return crud.update_discipline(db=db,discipline_id=discipline_id,discipline=discipline)
    else:
        return HTTPException(status_code=404, detail="Discipline not found")
   
#DELETE Discipline
@app.delete("/discipline/{discipline_id}")
def delete_discipline(discipline_id: int, db: Session = Depends(get_db)):
    db_discipline = crud.get_discipline(db=db,discipline_id=discipline_id)
    if db_discipline:
        return crud.delete_discipline(db=db,discipline=db_discipline)
    else:   
        return HTTPException(status_code=404, detail="Discipline not found")

#GET all Notes
@app.get("/notes/")
def read_notes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    notes = crud.get_notes(db, skip=skip, limit=limit)
    return notes

#GET Notes by discipline_id
@app.get("/notes/{discipline_id}")
def all_notes(discipline_id: int, db: Session = Depends(get_db)):
    db_discipline = crud.get_discipline(db=db,discipline_id=discipline_id)
    if db_discipline:
        return crud.get_notes_discipline(db=db,discipline_id=discipline_id)
    else:
        return HTTPException(status_code=404, detail="Discipline not found ")

#CREATE Discipline note
@app.post("/notes/{discipline_id}")
def create_note_for_discipline(discipline_id: int, note: schemas.NoteCreate, db: Session = Depends(get_db)):
    db_discipline = crud.get_discipline(db=db,discipline_id=discipline_id)
    if db_discipline:
        return crud.create_discipline_note(db=db, note=note, discipline_id=discipline_id)
    else:
        return HTTPException(status_code=404, detail="Discipline not found")

#ATT Discipline Note
@app.patch("/notes/{discipline_id}")
def update_note(discipline_id: int, note_id: int, note:schemas.NoteCreate, db: Session = Depends(get_db)):
    db_discipline = crud.get_discipline(db, discipline_id=discipline_id)
    if db_discipline:
        db_note = crud.get_notes_discipline(db=db,discipline_id=discipline_id)
        is_there = False
        for nota in db_note:
            if note_id == nota.id:
                is_there = True
        if is_there:
            print(note.description)
            print("-"*45)
            return crud.update_note(db=db,note_id=note_id,note=note)
        else:
            return HTTPException(status_code=404, detail="Note not found")
    else:
        return HTTPException(status_code=404, detail="Discipline not found")

#DELETE Note
@app.delete("/notes/{discipline_id}")
def delete_notes(discipline_id: int, note_id: int, db: Session = Depends(get_db)):
    db_discipline = crud.get_discipline(db=db,discipline_id=discipline_id)
    if db_discipline:
        db_note = crud.get_notes_discipline(db=db,discipline_id=discipline_id)
        is_there = False
        for nota in db_note:
            if note_id == nota.id:
                is_there = True
        if is_there:
            return crud.delete_note(db=db,note=db_note, discipline=db_discipline)
        else:
            return HTTPException(status_code=404, detail="Note not found")
    else:
        return HTTPException(status_code=404, detail="Discipline not found")
