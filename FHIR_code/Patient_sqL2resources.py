import sqlite3
import pandas as pd
from fhir.resources.patient import Patient
import json
import requests
from datetime import date

# Conectar a la base de datos SQLite
conn = sqlite3.connect('data/hospital_A.db')
cursor = conn.cursor()

# Extraer datos del paciente con id=1 y sus datos relacionados
query = """
SELECT p.id, p.name, p.dob, p.gender, p.address,
       d.code AS diag_code, d.description AS diag_desc, d.date AS diag_date, doc.name AS doctor_name,
       a.code AS allergy_code, a.substance, a.reaction, a.severity,
       m.code AS med_code, m.name AS med_name, m.dosage, m.start_date,
       c.insurer, c.policy_number, c.start_date AS coverage_start, c.end_date AS coverage_end
FROM Patients p
LEFT JOIN Diagnoses d ON p.id = d.patient_id
LEFT JOIN Doctors doc ON d.doctor_id = doc.id
LEFT JOIN AllergyIntolerances a ON p.id = a.patient_id
LEFT JOIN Medications m ON p.id = m.patient_id
LEFT JOIN Coverages c ON p.id = c.patient_id
WHERE p.id = 1;
"""
data = pd.read_sql_query(query, conn)

# Cerrar conexión
conn.close()

# Mostrar DataFrame
print("DataFrame del paciente:")
print(data)

# Mapear al recurso FHIR Patient
patient_data = data.iloc[0]  # Tomar la primera fila (paciente id=1)
patient = Patient.construct()
patient.id = str(patient_data['id'])
patient.name = [{'text': patient_data['name']}]
patient.birthDate = str(patient_data['dob'])
patient.gender = patient_data['gender'].lower()
patient.address = [{'text': patient_data['address']}]

# Serializar a JSON
patient_json_str = patient.json(indent=2)

# Mostrar el JSON
print("\nRecurso FHIR Patient en JSON:")
print(patient_json_str)



# Enviar al servidor HAPI FHIR
hapi_url = 'http://localhost:8080/fhir/Patient'
headers = {'Content-Type': 'application/fhir+json'}
response = requests.post(hapi_url, data=patient_json_str, headers=headers)

# Verificar respuesta
print("\nRespuesta del servidor HAPI FHIR:")
print(f"Status Code: {response.status_code}")
if response.status_code in [200, 201]:
    print("Paciente cargado exitosamente en HAPI FHIR.")
else:
    print(f"Error al cargar: {response.text}")