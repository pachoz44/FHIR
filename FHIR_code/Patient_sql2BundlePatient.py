import sqlite3
import requests
import uuid
import json

# ==========================================================
# CONFIGURACIÓN
# ==========================================================
DB_PATH = "FHIR_code\data\hospital_A.db"  # tu base de datos de la HCE
FHIR_SERVER = "http://localhost:8080/fhir"  # tu servidor HAPI FHIR

# ==========================================================
# FUNCIÓN: transforma fila SQL -> recurso Patient FHIR
# ==========================================================
def row_to_patient(row):
    patient_id = str(uuid.uuid4())  # generar un UUID temporal para el bundle

    return {
        "fullUrl": f"urn:uuid:{patient_id}",
        "resource": {
            "resourceType": "Patient",
            "id": patient_id,
            "name": [{
                "family": row["apellido"],
                "given": [row["nombre"]]
            }],
            "gender": "male" if row["gender"] == "M" else "female",
            "birthDate": row["dob"]
        },
        "request": {
            "method": "POST",
            "url": "Patient"
        }
    }

# ==========================================================
# 1. EXTRAER: leer pacientes de la HCE
# ==========================================================
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row  # acceso por nombre de columna
cursor = conn.cursor()

cursor.execute("SELECT id, nombre, apellido, dob, gender FROM Patients")
rows = cursor.fetchall()

print(f"Se encontraron {len(rows)} pacientes en la HCE")

# ==========================================================
# 2. TRANSFORMAR: filas -> entradas Bundle FHIR
# ==========================================================
entries = [row_to_patient(row) for row in rows]

bundle = {
    "resourceType": "Bundle",
    "type": "transaction",
    "entry": entries
}

# ==========================================================
# 3. CARGAR: enviar el Bundle al servidor HAPI FHIR
# ==========================================================
headers = {"Content-Type": "application/fhir+json"}

response = requests.post(FHIR_SERVER, headers=headers, data=json.dumps(bundle))

if response.status_code in [200, 201]:
    print("✅ Bundle cargado correctamente en HAPI FHIR")
    print(json.dumps(response.json(), indent=2))
else:
    print("❌ Error al cargar el Bundle")
    print(response.status_code, response.text)
