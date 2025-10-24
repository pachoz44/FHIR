import requests

FHIR_SERVER = "http://localhost:8080/fhir"
PATIENT_ID = "115"

url = f"{FHIR_SERVER}/Patient/{PATIENT_ID}/$everything"
headers = {"Accept": "application/fhir+json"}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    bundle = response.json()
    for entry in bundle.get("entry", []):
        resource = entry.get("resource", {})
        print(f"{resource['resourceType']}/{resource.get('id')}")
else:
    print(f"Error: {response.status_code}")


import requests
import json

FHIR_SERVER = "http://localhost:8080/fhir"
PATIENT_ID = "115"

url = f"{FHIR_SERVER}/Patient/{PATIENT_ID}/$everything"
headers = {"Accept": "application/fhir+json"}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    bundle = response.json()

    print(f"Se encontraron {len(bundle.get('entry', []))} recursos relacionados al Patient/{PATIENT_ID}\n")

    for entry in bundle.get("entry", []):
        resource = entry.get("resource", {})
        resource_type = resource.get("resourceType")
        resource_id = resource.get("id")

        print(f"==== {resource_type}/{resource_id} ====")
        print(json.dumps(resource, indent=2, ensure_ascii=False))  # imprime el JSON completo
        print("\n")
else:
    print(f"Error: {response.status_code} - {response.text}")
