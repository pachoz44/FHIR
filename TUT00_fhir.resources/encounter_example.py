from fhir.resources.encounter import Encounter
from fhir.resources.reference import FHIRReference
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.period import Period

# Referencias previas (de los recursos Patient y Practitioner)
patient_ref = FHIRReference(reference="Patient/example-001")
practitioner_ref = FHIRReference(reference="Practitioner/pract-001")

# Crear un Encounter
encounter = Encounter(
    id="enc-001",
    status="finished",
    class_fhir=Coding(  # Tipo de encuentro
        system="http://terminology.hl7.org/CodeSystem/v3-ActCode",
        code="AMB",
        display="Ambulatory"
    ),
    type=[
        CodeableConcept(
            coding=[Coding(
                system="http://snomed.info/sct",
                code="185349003",
                display="Consulta general ambulatoria"
            )]
        )
    ],
    subject=patient_ref,
    participant=[{
        "individual": practitioner_ref
    }],
    period=Period(start="2025-10-24T10:00:00Z", end="2025-10-24T10:30:00Z")
)

# Imprimir en formato JSON
print(encounter.json(indent=2))


with open("output/encounter.json", "w") as f:
    f.write(encounter.json(indent=2))