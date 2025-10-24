from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import requests

# URL del servidor FHIR (se inyecta desde docker-compose)
FHIR_SERVER_URL = os.getenv("FHIR_SERVER_URL", "http://localhost:8080/fhir")

app = FastAPI(
    title="FHIR Patient CRUD",
    description="CRUD básico de Patient en FHIR usando HAPI",
    version="1.0.0"
)

# Modelo simplificado de Patient
class Patient(BaseModel):
    id: str | None = None
    given: str
    family: str
    gender: str | None = None


@app.post("/patients", response_model=dict)
def create_patient(patient: Patient):
    fhir_patient = {
        "resourceType": "Patient",
        "name": [{"given": [patient.given], "family": patient.family}],
    }
    if patient.gender:
        fhir_patient["gender"] = patient.gender

    resp = requests.post(f"{FHIR_SERVER_URL}/Patient", json=fhir_patient)
    if resp.status_code not in (200, 201):
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp.json()


@app.get("/patients/{patient_id}", response_model=dict)
def get_patient(patient_id: str):
    resp = requests.get(f"{FHIR_SERVER_URL}/Patient/{patient_id}")
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp.json()


@app.put("/patients/{patient_id}", response_model=dict)
def update_patient(patient_id: str, patient: Patient):
    fhir_patient = {
        "resourceType": "Patient",
        "id": patient_id,
        "name": [{"given": [patient.given], "family": patient.family}],
    }
    if patient.gender:
        fhir_patient["gender"] = patient.gender

    resp = requests.put(f"{FHIR_SERVER_URL}/Patient/{patient_id}", json=fhir_patient)
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp.json()


@app.delete("/patients/{patient_id}", response_model=dict)
def delete_patient(patient_id: str):
    resp = requests.delete(f"{FHIR_SERVER_URL}/Patient/{patient_id}")
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return {"msg": f"Patient {patient_id} eliminado"}
