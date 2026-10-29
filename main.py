from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Bug Tracker API")

class Bug(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    status: str = "open"

bugs_db = []
id_counter = 1

@app.get("/")
def read_root():
    return {"message": "Welcome to Bug Tracker API"}

@app.get("/bugs", response_model=List[Bug])
def get_bugs():
    return bugs_db

@app.post("/bugs", response_model=Bug, status_code=201)
def create_bug(bug: Bug):
    global id_counter
    bug.id = id_counter
    id_counter += 1
    bugs_db.append(bug)
    return bug

@app.get("/bugs/{bug_id}", response_model=Bug)
def get_bug(bug_id: int):
    for bug in bugs_db:
        if bug.id == bug_id:
            return bug
    raise HTTPException(status_code=404, detail="Bug not found")

@app.put("/bugs/{bug_id}", response_model=Bug)
def update_bug(bug_id: int, updated_bug: Bug):
    for idx, bug in enumerate(bugs_db):
        if bug.id == bug_id:
            updated_bug.id = bug_id
            bugs_db[idx] = updated_bug
            return updated_bug
    raise HTTPException(status_code=404, detail="Bug not found")

@app.delete("/bugs/{bug_id}")
def delete_bug(bug_id: int):
    for idx, bug in enumerate(bugs_db):
        if bug.id == bug_id:
            bugs_db.pop(idx)
            return {"message": "Bug deleted"}
    raise HTTPException(status_code=404, detail="Bug not found")
