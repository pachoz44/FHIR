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
    return None  # si no encuentra, devolvemos None

# === Función para mapear medicamento a ATC ===
def map_to_atc(texto):
    texto_norm = normalize_text(texto)
    for key, (code, display) in atc_map.items():
        if key in texto_norm:
            return {"system": "http://www.whocc.no/atc", "code": code, "display": display}
    return None  # si no encuentra, devolvemos None

# === Cargar CSV ===
df = pd.read_csv("consultas_pacientes.csv")

# === Generar Bundles por paciente (transaction) ===
for _, row in df.iterrows():
    patient_id = f"patient-{row['Cedula']}"
    encounter_id = f"encounter-{row['Cedula']}-1"

    # Mapear diagnóstico principal
    diag_coding = map_to_snomed(str(row["Diagnósticos"]))

    bundle = {
        "resourceType": "Bundle",
        "type": "transaction",
        "entry": []
    }

    # Patient
    patient = {
        "resourceType": "Patient",
        "id": patient_id,
        "identifier": [
            {"system": "http://hospital.org/cedula", "value": str(row["Cedula"])},
            {"system": "http://hospital.org/coddactilar", "value": str(row["CodDactilar"])}
        ],
        "name": [{"use": "official","family": row["Apellido"],"given": [row["Nombre"]]}],
        "gender": "female" if normalize_text(row["Sexo"]).startswith("f") else "male"
    }
    bundle["entry"].append({
        "resource": patient,
        "request": {"method": "POST", "url": "Patient"}
    })

    # Encounter
    encounter = {
        "resourceType": "Encounter",
        "id": encounter_id,
        "status": "finished",
        "class": {"system": "http://terminology.hl7.org/CodeSystem/v3-ActCode", "code": "AMB"},
        "subject": {"reference": f"Patient/{patient_id}"},
        "reasonCode": [{"coding": [diag_coding] if diag_coding else [], "text": row["Motivo de consulta"]}],
        "period": {"start": datetime.now().isoformat()}
    }
    bundle["entry"].append({
        "resource": encounter,
        "request": {"method": "POST", "url": "Encounter"}
    })

    # Condition
    condition = {
        "resourceType": "Condition",
        "id": f"condition-{row['Cedula']}-1",
        "clinicalStatus": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-clinical", "code": "active"}]},
        "verificationStatus": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-ver-status", "code": "confirmed"}]},
        "code": {
            "coding": [diag_coding] if diag_coding else [],
            "text": row["Diagnósticos"]
        },
        "subject": {"reference": f"Patient/{patient_id}"},
        "encounter": {"reference": f"Encounter/{encounter_id}"}
    }
    bundle["entry"].append({
        "resource": condition,
        "request": {"method": "POST", "url": "Condition"}
    })

    # MedicationRequest (si aplica)
    if isinstance(row["Prescripciones"], str) and row["Prescripciones"].strip():
        med_coding = map_to_atc(row["Prescripciones"])
        medication = {
            "resourceType": "MedicationRequest",
            "id": f"medication-{row['Cedula']}-1",
            "status": "active",
            "intent": "order",
            "medicationCodeableConcept": {
                "coding": [med_coding] if med_coding else [],
                "text": row["Prescripciones"]
            },
            "subject": {"reference": f"Patient/{patient_id}"},
            "encounter": {"reference": f"Encounter/{encounter_id}"},
            "authoredOn": datetime.now().date().isoformat(),
            "dosageInstruction": [{"text": row["Prescripciones"]}]
        }
        bundle["entry"].append({
            "resource": medication,
            "request": {"method": "POST", "url": "MedicationRequest"}
        })

    # CarePlan
    careplan = {
        "resourceType": "CarePlan",
        "id": f"careplan-{row['Cedula']}-1",
        "status": "active",
        "intent": "plan",
        "subject": {"reference": f"Patient/{patient_id}"},
        "encounter": {"reference": f"Encounter/{encounter_id}"},
        "description": row["Recomendaciones"]
    }
    bundle["entry"].append({
        "resource": careplan,
        "request": {"method": "POST", "url": "CarePlan"}
    })

    # Observation
    observation = {
        "resourceType": "Observation",
        "id": f"observation-{row['Cedula']}-1",
        "status": "final",
        "code": {"text": "Evolución clínica"},
        "subject": {"reference": f"Patient/{patient_id}"},
        "encounter": {"reference": f"Encounter/{encounter_id}"},
        "valueString": row["Evolución"]
    }
    bundle["entry"].append({
        "resource": observation,
        "request": {"method": "POST", "url": "Observation"}
    })

    # Guardar en archivo
    file_name = f"jsonbundles/bundle_{row['Cedula']}.json"
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=2, ensure_ascii=False)

    print(f"✅ Bundle transaction generado: {file_name}")
