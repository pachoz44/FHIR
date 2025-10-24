from azure.identity import ClientSecretCredential
import requests
import json

# ===== Configuración =====
FHIR_URL = "https://fhirworkspace593-fhirservice.fhir.azurehealthcareapis.com"
TENANT_ID = "e94a7344-127e-4ba2-b995-24410a5be1de"
CLIENT_ID = "69462078-c9fb-45cd-90fa-90f1facaee41"
CLIENT_SECRET = "uVS8Q~UwzX7~6qsTdF.zLYLmNL9VoNWZzlIR_c4G"

# Aquí pones el identificador del paciente (por ejemplo cédula)
PATIENT_IDENTIFIER = "20252025"  

# ===== Autenticación =====
credential = ClientSecretCredential(
    tenant_id=TENANT_ID,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)

scope = f"{FHIR_URL}/.default"
token = credential.get_token(scope).token

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/fhir+json"
}

# ===== Función para manejar paginación =====
def fetch_all_resources(url):
    all_entries = []
    while url:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Error {response.status_code}: {response.text}")
        bundle = response.json()
        entries = bundle.get("entry", [])
        all_entries.extend(entries)
        
        # Buscar link "next" para paginación
        next_link = None
        for link in bundle.get("link", []):
            if link.get("relation") == "next":
                next_link = link.get("url")
                break
        url = next_link
    return all_entries

# ===== Buscar paciente por identifier =====
search_url = f"{FHIR_URL}/Patient?identifier={PATIENT_IDENTIFIER}"
response = requests.get(search_url, headers=headers)
patients_bundle = response.json()

if "entry" not in patients_bundle or len(patients_bundle["entry"]) == 0:
    raise Exception(f"No se encontró paciente con identifier {PATIENT_IDENTIFIER}")

patient_resource = patients_bundle["entry"][0]["resource"]
patient_id = patient_resource["id"]
print(f"Paciente encontrado: {patient_id} ({patient_resource.get('name', [{}])[0].get('text', 'Sin nombre')})")

# ===== Obtener todos los recursos con $everything =====
everything_url = f"{FHIR_URL}/Patient/{patient_id}/$everything"
all_resources = fetch_all_resources(everything_url)

print(f"Total recursos obtenidos: {len(all_resources)}")

# ===== Guardar en archivo JSON =====
filename = f"Patient_{patient_id}_everything.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(all_resources, f, indent=2, ensure_ascii=False)

print(f"Recursos guardados en {filename}")
