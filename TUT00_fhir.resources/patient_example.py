import json
from fhir.resources.patient import Patient
from fhir.resources.humanname import HumanName
from fhir.resources.contactpoint import ContactPoint

# Crear un recurso Patient
patient = Patient(
    id="example-001",
    active=True,
    gender="male",
    birthDate="1980-03-10",
    name=[HumanName(family="Doe", given=["John"])],
    telecom=[ContactPoint(system="phone", value="+593999888777", use="mobile")]
)

# Convertir a JSON FHIR
patient_json = patient.json(indent=2)
print(patient_json)
