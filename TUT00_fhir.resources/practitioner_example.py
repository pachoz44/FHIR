from fhir.resources.practitioner import Practitioner
from fhir.resources.humanname import HumanName
from fhir.resources.contactpoint import ContactPoint
from fhir.resources.address import Address

# Crear un recurso Practitioner
practitioner = Practitioner(
    id="pract-001",
    active=True,
    name=[HumanName(family="Zuniga", given=["Fernando", "Andrés"])],
    telecom=[
        ContactPoint(system="email", value="fzhuniga@hospital.ec", use="work"),
        ContactPoint(system="phone", value="+593999555444", use="mobile")
    ],
    address=[
        Address(
            line=["Av. Amazonas 1234"],
            city="Quito",
            country="Ecuador"
        )
    ],
    gender="male"
)

# Imprimir en formato JSON
print(practitioner.json(indent=2))


with open("output/practitioner.json", "w") as f:
    f.write(practitioner.json(indent=2))