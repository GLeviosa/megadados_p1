from typing import List, Optional

from pydantic import BaseModel


# NOTES

class NoteBase (BaseModel):
    description: str = None

class NoteCreate(NoteBase):
    pass

class Note(NoteBase):
    discipline_id:int
    id:int
    class Config:
        orm_mode = True

# DISCIPLINES

class DisciplineBase (BaseModel):
    name:str = None
    professor:Optional[str]  = None
    notes: List[Note] = []


class DisciplineCreate(DisciplineBase):
    pass

class Discipline(DisciplineBase):
    id:int
    class Config:
        orm_mode = True

