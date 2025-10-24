import pandas as pd
import json
from datetime import datetime
import unicodedata

# === Diccionario de diagnósticos a SNOMED CT ===
snomed_map = {
    "trastornos mentales y del comportamiento debido al consumo de múltiples drogas": ("268631001", "Mental and behavioural disorders due to multiple drug use"),
    "trastorno depresivo de la conducta": ("35489007", "Depressive disorder"),
    "cuadro depresivo": ("35489007", "Depressive disorder"),
    "trastorno de ansiedad no especificado": ("197480006", "Anxiety disorder, unspecified"),
    "ansiedad": ("197480006", "Anxiety disorder"),
    "crisis de ansiedad": ("225624000", "Panic attack"),
    "insomnio": ("193462001", "Insomnia"),
    "dificultad para dormir": ("193462001", "Insomnia"),
    "desvelo constante": ("193462001", "Insomnia"),
    "abstinencia": ("91175000", "Drug withdrawal syndrome"),
    "tos húmeda": ("28743005", "Productive cough"),
    "aislamiento social": ("248062006", "Social isolation"),
    "pérdida de interés": ("366979004", "Anhedonia")
}

# === Diccionario de medicamentos a ATC ===
atc_map = {
    "risperidona": ("N05AX08", "Risperidone"),
    "fluoxetina": ("N06AB03", "Fluoxetine"),
    "sertralina": ("N06AB06", "Sertraline"),
    "clonazepam": ("N03AE01", "Clonazepam")
}

# === Normalización de texto ===
def normalize_text(text):
    text = str(text).lower()
    text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    return text

# === Función para mapear diagnóstico a SNOMED ===
def map_to_snomed(texto):
    texto_norm = normalize_text(texto)
    for key, (code, display) in snomed_map.items():
        if normalize_text(key) in texto_norm:
            return {"system": "http://snomed.info/sct", "code": code, "display": display}
    return None

# === Función para mapear medicamento a ATC ===
def map_to_atc(texto):
    texto_norm = normalize_text(texto)
    for key, (code, display) in atc_map.items():
        if key in texto_norm:
            return {"system": "http://www.whocc.no/atc", "code": code, "display": display}
    return None

# === Cargar CSV ===
df = pd.read_csv("consultas_pacientes.csv")

# === Generar Bundles por paciente (transaction) con fullUrl ===
for _, row in df.iterrows():
    patient_uuid = f"urn:uuid:patient-{row['Cedula']}"
    encounter_uuid = f"urn:uuid:encounter-{row['Cedula']}-1"
    condition_uuid = f"urn:uuid:condition-{row['Cedula']}-1"
    medication_uuid = f"urn:uuid:medication-{row['Cedula']}-1"
    careplan_uuid = f"urn:uuid:careplan-{row['Cedula']}-1"
    observation_uuid = f"urn:uuid:observation-{row['Cedula']}-1"

    diag_coding = map_to_snomed(str(row["Diagnósticos"]))
    med_coding = map_to_atc(str(row["Prescripciones"])) if isinstance(row["Prescripciones"], str) else None

    bundle = {
        "resourceType": "Bundle",
        "type": "transaction",
        "entry": []
    }

    # Patient
    patient = {
        "resourceType": "Patient",
        "id": f"patient-{row['Cedula']}",
        "identifier": [
            {"system": "http://hospital.org/cedula", "value": str(row["Cedula"])},
            {"system": "http://hospital.org/coddactilar", "value": str(row["CodDactilar"])}
        ],
        "name": [{"use": "official","family": row["Apellido"],"given": [row["Nombre"]]}],
        "gender": "female" if normalize_text(row["Sexo"]).startswith("f") else "male"
    }
    bundle["entry"].append({
        "fullUrl": patient_uuid,
        "resource": patient,
        "request": {"method": "POST", "url": "Patient"}
    })

    # Encounter
    encounter = {
        "resourceType": "Encounter",
        "id": f"encounter-{row['Cedula']}-1",
        "status": "finished",
        "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "AMB"},
        "subject": {"reference": patient_uuid},
        "reasonCode": [{"coding": [diag_coding] if diag_coding else [], "text": row["Motivo de consulta"]}],
        "period": {"start": datetime.now().isoformat()}
    }
    bundle["entry"].append({
        "fullUrl": encounter_uuid,
        "resource": encounter,
        "request": {"method": "POST", "url": "Encounter"}
    })

    # Condition
    condition = {
        "resourceType": "Condition",
        "id": f"condition-{row['Cedula']}-1",
        "clinicalStatus": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-clinical", "code": "active"}]},
        "verificationStatus": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-ver-status", "code": "confirmed"}]},
        "code": {"coding": [diag_coding] if diag_coding else [], "text": row["Diagnósticos"]},
        "subject": {"reference": patient_uuid},
        "encounter": {"reference": encounter_uuid}
    }
    bundle["entry"].append({
        "fullUrl": condition_uuid,
        "resource": condition,
        "request": {"method": "POST", "url": "Condition"}
    })

    # MedicationRequest (si aplica)
    if med_coding:
        medication = {
            "resourceType": "MedicationRequest",
            "id": f"medication-{row['Cedula']}-1",
            "status": "active",
            "intent": "order",
            "medicationCodeableConcept": {"coding": [med_coding], "text": row["Prescripciones"]},
            "subject": {"reference": patient_uuid},
            "encounter": {"reference": encounter_uuid},
            "authoredOn": datetime.now().date().isoformat(),
            "dosageInstruction": [{"text": row["Prescripciones"]}]
        }
        bundle["entry"].append({
            "fullUrl": medication_uuid,
            "resource": medication,
            "request": {"method": "POST", "url": "MedicationRequest"}
        })

    # CarePlan
    careplan = {
        "resourceType": "CarePlan",
        "id": f"careplan-{row['Cedula']}-1",
        "status": "active",
        "intent": "plan",
        "subject": {"reference": patient_uuid},
        "encounter": {"reference": encounter_uuid},
        "description": row["Recomendaciones"]
    }
    bundle["entry"].append({
        "fullUrl": careplan_uuid,
        "resource": careplan,
        "request": {"method": "POST", "url": "CarePlan"}
    })

    # Observation
    observation = {
        "resourceType": "Observation",
        "id": f"observation-{row['Cedula']}-1",
        "status": "final",
        "code": {"text": "Evolución clínica"},
        "subject": {"reference": patient_uuid},
        "encounter": {"reference": encounter_uuid},
        "valueString": row["Evolución"]
    }
    bundle["entry"].append({
        "fullUrl": observation_uuid,
        "resource": observation,
        "request": {"method": "POST", "url": "Observation"}
    })

    # Guardar en archivo
    file_name = f"jsonbundles/bundle_{row['Cedula']}.json"
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=2, ensure_ascii=False)

    print(f"✅ Bundle transaction generado: {file_name}")
