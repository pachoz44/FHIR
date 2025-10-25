from fhir.resources.observation import Observation
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.reference import FHIRReference
from fhir.resources.quantity import Quantity

# Referencias a otros recursos
patient_ref = FHIRReference(reference="Patient/example-001")
encounter_ref = FHIRReference(reference="Encounter/enc-001")

# Crear el recurso Observation
observation = Observation(
    id="obs-001",
    status="final",
    category=[CodeableConcept(
        coding=[Coding(
            system="http://terminology.hl7.org/CodeSystem/observation-category",
            code="vital-signs",
            display="Signos vitales"
        )]
    )],
    code=CodeableConcept(
        coding=[Coding(
            system="http://loinc.org",
            code="8310-5",
            display="Body temperature"
        )],
        text="Temperatura corporal"
    ),
    subject=patient_ref,
    encounter=encounter_ref,
    effectiveDateTime="2025-10-24T10:10:00Z",
    valueQuantity=Quantity(
        value=36.8,
        unit="°C",
        system="http://unitsofmeasure.org",
        code="Cel"
    )
)

print(observation.json(indent=2))

with open("output/observation.json", "w") as f:
    f.write(observation.json(indent=2))
