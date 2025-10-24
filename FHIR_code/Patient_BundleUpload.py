import os
import requests
import json

# === Configuración del servidor FHIR ===
FHIR_SERVER = "http://localhost:8080/fhir"  # cambia la URL si tu servidor corre en otro puerto o en la nube
BUNDLE_DIR = "jsonbundles"  # carpeta donde están los bundles generados

# Crear sesión HTTP
session = requests.Session()
session.headers.update({"Content-Type": "application/fhir+json"})

# Iterar sobre los archivos en la carpeta
for filename in os.listdir(BUNDLE_DIR):
    if filename.endswith(".json"):
        file_path = os.path.join(BUNDLE_DIR, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            bundle = json.load(f)
        
        # POST al servidor FHIR
        response = session.post(FHIR_SERVER, json=bundle)
        
        if response.status_code in [200, 201]:
            print(f"✅ {filename} cargado correctamente en FHIR.")
        else:
            print(f"❌ Error cargando {filename}: {response.status_code}")
            print(response.text)
