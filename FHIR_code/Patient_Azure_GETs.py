import os
from azure.identity import ClientSecretCredential
import requests
import json

# ===== Configuración =====
FHIR_URL = "https://fhirworkspace593-fhirservice.fhir.azurehealthcareapis.com"
TENANT_ID = "e94a7344-127e-4ba2-b995-24410a5be1de"
CLIENT_ID = "69462078-c9fb-45cd-90fa-90f1facaee41"
CLIENT_SECRET = "uVS8Q~UwzX7~6qsTdF.zLYLmNL9VoNWZzlIR_c4G"

BUNDLE_FOLDER = "jsonbundles"  # Carpeta donde están los Bundles

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
    "Accept": "application/fhir+json",
    "Content-Type": "application/fhir+json"
}

# ===== Función para manejar paginación =====
def fetch_all_resources(url):
    all_entries = []
    while url:
        resp = requests.get(url, headers={"Authorization": f"Bearer {token}", "Accept": "application/fhir+json"})
        if resp.status_code != 200:
            raise Exception(f"Error {resp.status_code}: {resp.text}")
        b = resp.json()
        entries = b.get("entry", [])
        all_entries.extend(entries)
        # Buscar link "next" para paginación
        next_link = None
        for link in b.get("link", []):
            if link.get("relation") == "next":
                next_link = link.get("url")
                break
        url = next_link
    return all_entries

# ===== Procesar todos los Bundles en la carpeta =====
for filename in os.listdir(BUNDLE_FOLDER):
    if not filename.endswith(".json"):
        continue

    bundle_path = os.path.join(BUNDLE_FOLDER, filename)
    with open(bundle_path, "r", encoding="utf-8") as f:
        bundle_data = json.load(f)

    # Subir Bundle a Azure FHIR
    response = requests.post(f"{FHIR_URL}/", headers=headers, json=bundle_data)
    if response.status_code not in [200, 201]:
        print(f"Error al subir {filename}: {response.status_code} {response.text}")
        continue
    print(f"Bundle {filename} cargado correctamente")

    # ===== Buscar el Patient ID por identifier =====
    # Asumimos que el primer Patient del Bundle tiene el primer identifier que usamos
    patient_identifier = bundle_data["entry"][0]["resource"]["identifier"][0]["value"]
    search_url = f"{FHIR_URL}/Patient?identifier={patient_identifier}"
    resp = requests.get(search_url, headers={"Authorization": f"Bearer {token}", "Accept": "application/fhir+json"})
    if resp.status_code != 200:
        print(f"Error al buscar paciente en {filename}: {resp.status_code} {resp.text}")
        continue

    patients = resp.json()
    if "entry" not in patients or len(patients["entry"]) == 0:
        print(f"No se encontró paciente con identifier {patient_identifier} en {filename}")
        continue

    patient_id = patients["entry"][0]["resource"]["id"]
    print(f"Patient ID real encontrado: {patient_id}")

    # ===== Ejecutar $everything =====
    everything_url = f"{FHIR_URL}/Patient/{patient_id}/$everything"
    all_resources = fetch_all_resources(everything_url)
    print(f"Total recursos obtenidos para {patient_id}: {len(all_resources)}")

    # ===== Guardar recursos en JSON =====
    output_file = f"Patient_{patient_id}_everything.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_resources, f, indent=2, ensure_ascii=False)

    print(f"Recursos guardados en {output_file}\n")
