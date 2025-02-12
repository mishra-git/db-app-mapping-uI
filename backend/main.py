from fastapi import FastAPI
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import cursor, conn  # ✅ Correct
from pydantic import BaseModel
from database import get_all_mappings, add_mapping, update_mapping, delete_mapping # Ensure this matches your folder structure
import logging


app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Model
class Mapping(BaseModel):
    application_name: str
    database_name: str
    instance_name: str
    database_type: str
    team_name: str
    environment: str
    server_owner: str
    database_owner: str
    application_contacts: str

# ✅ Fetch all mappings
@app.get("/mappings")
def get_mappings():
    data = get_all_mappings()
    if isinstance(data, dict) and "error" in data:
        raise HTTPException(status_code=500, detail=data["error"])
    return data

# ✅ Add a new mapping
@app.post("/mappings")
def create_mapping(mapping: Mapping):
    data = add_mapping(
        mapping.application_name, mapping.database_name, mapping.instance_name,
        mapping.database_type, mapping.team_name, mapping.environment,
        mapping.server_owner, mapping.database_owner, mapping.application_contacts
    )
    if "error" in data:
        raise HTTPException(status_code=500, detail=data["error"])
    return data

# ✅ Update a mapping
@app.put("/mappings/{mapping_id}")
def modify_mapping(mapping_id: int, mapping: Mapping):
    data = update_mapping(
        mapping_id, mapping.application_name, mapping.database_name,
        mapping.instance_name, mapping.database_type, mapping.team_name,
        mapping.environment, mapping.server_owner, mapping.database_owner,
        mapping.application_contacts
    )
    if "error" in data:
        raise HTTPException(status_code=500, detail=data["error"])
    return data

# ✅ Delete a mapping
@app.delete("/mappings/{mapping_id}")
def remove_mapping(mapping_id: int):
    data = delete_mapping(mapping_id)
    if "error" in data:
        raise HTTPException(status_code=500, detail=data["error"])
    return data
