from typing import Optional, List

from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

class Discipline(BaseModel):
    name : str
    professor : Optional[str] = None
    notes : List[str]

dic = {}
success = {"status" : 200,
           "response" : {} }

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/disciplines/{discipline_id}")
def read_discipline(discipline_id: int):
    success["response"] = dic[discipline_id]
    return success

# Cria Disciplina
@app.post("/disciplines/")
async def create_discipline(discipline : Discipline):
    if 0 not in dic:
        dic[0] = discipline
    else:
        is_in_dic = False
        for key, value in dic.items():
            if discipline.name == value.name:
                is_in_dic = True
        if is_in_dic:
            raise HTTPException(status_code=409, detail="Conflict, Already exists")
        else:    
            new_index = list(dic)[-1] + 1
            dic[new_index] = discipline

    success["response"] = dic
    return success

# Atualiza Disciplina
@app.put("/disciplines/{discipline_id}")
async def update_discipline(discipline : Discipline, discipline_id: int):
    dic[discipline_id] = discipline
    return dic

# Deleta Disciplina
@app.delete("/disciplines/{discipline_id}")
async def delete_discipline(discipline_id : int):
    deleted = dic.pop(discipline_id, False)
    if deleted:
        success["response"] = dic
        return success
    else:
        raise HTTPException(status_code=404, detail="ID not found")

# Lista Disciplinas
@app.get("/disciplines/")
def show_all():
    names = {
        "disciplines" : []
    }
    for value in dic.values():
        names["disciplines"].append(value.name)
    return names

@app.patch("/notes/{discipline_id}")
def add_note(discipline_id : int, note : str):
    if discipline_id not in dic:
        raise HTTPException(status_code=404, detail="ID not found")
        
    dic[discipline_id].notes.append(note)
    success["response"] = dic
    return success

@app.delete("/notes/{discipline_id}")
def remove_note(discipline_id : int, note_index : int):
    if discipline_id not in dic:
        raise HTTPException(status_code=404, detail="Discipline_ID not found")
    if note_index > len(dic[discipline_id].notes) -1:
        raise HTTPException(status_code=404, detail="Note_ID not found")
    dic[discipline_id].notes.pop(note_index)
    success["response"] = dic
    return success

@app.get("/notes/{discipline_id}")
def show_notes(discipline_id : int):
    if discipline_id not in dic:
        raise HTTPException(status_code=404, detail="ID not found")
    response = {
        "notes" : dic[discipline_id].notes
    }
    return response

@app.patch("/notes/{discipline_id}")
def mod_note(discipline_id : int, note_index : int, new_note : str):
    if discipline_id not in dic:
        raise HTTPException(status_code=404, detail="Discipline_ID not found")
    if note_index > len(dic[discipline_id].notes) -1:
        raise HTTPException(status_code=404, detail="Note_ID not found")
    dic[discipline_id].notes[note_index] = new_note

    success["response"] = dic
    return success
    
# @app.put("/items/{item_id}")
# async def create_item(item_id: int, item: Item):
#     return {"item_id": item_id, **item.dict()}