import os
import json
import requests

# ===========================
# Configuración
# ===========================
FHIR_URL = "https://fhirworkspace593-fhirservice.fhir.azurehealthcareapis.com"
TENANT_ID = "e94a7344-127e-4ba2-b995-24410a5be1de"
CLIENT_ID = "69462078-c9fb-45cd-90fa-90f1facaee41"
CLIENT_SECRET = "uVS8Q~UwzX7~6qsTdF.zLYLmNL9VoNWZzlIR_c4G"
BUNDLE_DIR = "jsonbundles"  # Carpeta donde están los bundles generados

# ===========================
# 1️⃣ Obtener token de Azure AD
# ===========================
token_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/token"
data = {
    "grant_type": "client_credentials",
    "resource": FHIR_URL,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "scope": f"{FHIR_URL}/.default"
}

resp = requests.post(token_url, data=data)
if resp.status_code != 200:
    raise Exception(f"Error obteniendo token: {resp.status_code} {resp.text}")

access_token = resp.json()["access_token"]
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/fhir+json"
}

print("✅ Token obtenido correctamente")

# ===========================
# 2️⃣ Subir bundles a Azure FHIR
# ===========================
for file_name in os.listdir(BUNDLE_DIR):
    if file_name.endswith(".json"):
        file_path = os.path.join(BUNDLE_DIR, file_name)
        with open(file_path, "r", encoding="utf-8") as f:
            bundle = json.load(f)

        response = requests.post(f"{FHIR_URL}/", headers=headers, json=bundle)
        if response.status_code in [200, 201]:
            print(f"✅ Bundle subido correctamente: {file_name}")
            # Guardar respuesta del servidor si quieres
            resp_file = os.path.join(BUNDLE_DIR, f"uploaded_{file_name}")
            with open(resp_file, "w", encoding="utf-8") as f:
                json.dump(response.json(), f, indent=2, ensure_ascii=False)
        else:
            print(f"❌ Error subiendo {file_name}: {response.status_code} {response.text}")
