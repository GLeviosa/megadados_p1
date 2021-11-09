from typing import Optional, List

from fastapi import FastAPI, Path, Query, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
import json

app = FastAPI()

class Discipline(BaseModel):
    name : str
    professor : Optional[str] = None
    notes : List[str]

dic = {}
with open("db_local.json", "r") as file:
    dic = json.load(file)


success = {"status" : 200,
           "response" : {} }

def att_db(dic):
    dic_json = jsonable_encoder(dic)
    dic_object = json.dumps(dic_json, indent=4)
    with open("db_local.json", "w") as file:
        file.write(dic_object)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/disciplines/{discipline_id}")
def read_discipline(discipline_id: str):
    if discipline_id not in dic:
        raise HTTPException(status_code=404, detail="discipline_id not found")
    success["response"] = dic[discipline_id]
    return success

# Cria Disciplina
@app.post("/disciplines/")
async def create_discipline(discipline : Discipline):
    if "0" not in dic:
        dic["0"] = dict(discipline)
    else:
        is_in_dic = False
        for key, value in dic.items():
            if discipline.name == value["name"]:
                is_in_dic = True
        if is_in_dic:
            raise HTTPException(status_code=409, detail="Conflict, Already exists")
        else:    
            new_index = str(int(list(dic)[-1]) + 1)
            dic[new_index] = dict(discipline)

    success["response"] = dic
    att_db(dic)
    return success

# Atualiza Disciplina
@app.put("/disciplines/{discipline_id}")
async def update_discipline(discipline : Discipline, discipline_id: str):
    if discipline_id not in dic:
        raise HTTPException(status_code=404, detail="discipline_id not found")
    dic[discipline_id] = dict(discipline)
    att_db(dic)
    return dic

# Deleta Disciplina
@app.delete("/disciplines/{discipline_id}")
async def delete_discipline(discipline_id : str):
    deleted = dic.pop(discipline_id, False)
    if deleted:
        success["response"] = dic
        att_db(dic)
        return success
    else:
        raise HTTPException(status_code=404, detail="discipline_id not found")

# Lista Disciplinas
@app.get("/disciplines/")
def show_all():
    names = {
        "disciplines" : []
    }
    for value in dic.values():
        names["disciplines"].append(value["name"])
    return names

# Deleta disciplina
@app.delete("/notes/{discipline_id}")
def remove_note(discipline_id : str, note_index : int):
    if discipline_id not in dic:
        raise HTTPException(status_code=404, detail="Discipline_ID not found")
    if note_index > len(dic[discipline_id]["notes"]) -1:
        raise HTTPException(status_code=404, detail="note_index doesn't exist")
    dic[discipline_id]["notes"].pop(note_index)
    success["response"] = dic
    att_db(dic)
    return success

# Get notas
@app.get("/notes/{discipline_id}")
def show_notes(discipline_id : str):
    if discipline_id not in dic:
        raise HTTPException(status_code=404, detail="discipline_id not found")
    response = {
        "name"  : dic[discipline_id]["name"],
        "notes" : dic[discipline_id]["notes"]
    }
    success["response"] = response
    return success

@app.post("/notes/{discipline_id}")
def add_note(discipline_id : str, new_note : str):
    if discipline_id not in dic:
        raise HTTPException(status_code=404, detail="discipline_id not found")
    dic[discipline_id]["notes"].append(new_note)
    
    success["response"] = dic
    att_db(dic)
    return success

@app.put("/notes/{discipline_id}")
def mod_note(discipline_id : str, note_index : int, new_note : str):
    print(new_note)
    print("-"*15)
    if discipline_id not in dic:
        raise HTTPException(status_code=404, detail="discipline_id not found")
    if note_index > len(dic[discipline_id]["notes"]) -1:
        raise HTTPException(status_code=404, detail="note_index doesn't exist")
    dic[discipline_id]["notes"][note_index] = new_note

    success["response"] = dic
    att_db(dic)
    return success
    
