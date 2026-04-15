"""Legacy reference seeding script kept outside the migrations package."""

from django.core.management.base import BaseCommand

from echo_nt.fauna.models import ConservationStatus, Habitat, Species


SPECIES_DATA = [
    {
        "name": "Saltwater Crocodile",
        "scientific_name": "Crocodylus porosus",
        "conservation_status": ConservationStatus.LEAST_CONCERN,
        "summary": "Large apex reptile common in NT estuaries, floodplains, and coastal wetlands.",
        "habitats": ["Estuary", "River", "Wetland"],
    },
    {
        "name": "Northern Quoll",
        "scientific_name": "Dasyurus hallucatus",
        "conservation_status": ConservationStatus.ENDANGERED,
        "summary": "A carnivorous marsupial whose NT populations are under pressure from cane toads and fire regimes.",
        "habitats": ["Savanna Woodland", "Rocky Escarpment"],
    },
    {
        "name": "Red Kangaroo",
        "scientific_name": "Osphranter rufus",
        "conservation_status": ConservationStatus.LEAST_CONCERN,
        "summary": "Australia's largest marsupial, widespread in arid and semi-arid parts of the Territory.",
        "habitats": ["Desert Plain", "Grassland"],
    },
    {
        "name": "Brolga",
        "scientific_name": "Antigone rubicunda",
        "conservation_status": ConservationStatus.LEAST_CONCERN,
        "summary": "Tall wetland crane famous for pair dancing displays across northern floodplains.",
        "habitats": ["Wetland", "Floodplain"],
    },
    {
        "name": "Kakadu Plum",
        "scientific_name": "Terminalia ferdinandiana",
        "conservation_status": ConservationStatus.LEAST_CONCERN,
        "summary": "Iconic native NT tree valued for its fruit and cultural significance.",
        "habitats": ["Open Woodland", "Floodplain Edge"],
    },
    {
        "name": "Black-footed Tree-rat",
        "scientific_name": "Mesembriomys gouldii",
        "conservation_status": ConservationStatus.ENDANGERED,
        "summary": "Large arboreal rodent that persists in patches of northern savanna and monsoon forest.",
        "habitats": ["Monsoon Forest", "Savanna Woodland"],
    },
    {
        "name": "Bilby",
        "scientific_name": "Macrotis lagotis",
        "conservation_status": ConservationStatus.VULNERABLE,
        "summary": "Nocturnal digging marsupial recorded in parts of the Tanami and central deserts.",
        "habitats": ["Desert Plain", "Spinifex Grassland"],
    },
    {
        "name": "Emu",
        "scientific_name": "Dromaius novaehollandiae",
        "conservation_status": ConservationStatus.LEAST_CONCERN,
        "summary": "Large flightless bird that uses open habitats and seasonal resource pulses.",
        "habitats": ["Grassland", "Open Woodland"],
    },
    {
        "name": "Agile Wallaby",
        "scientific_name": "Notamacropus agilis",
        "conservation_status": ConservationStatus.LEAST_CONCERN,
        "summary": "Common wallaby in Top End grasslands, woodlands, and floodplain margins.",
        "habitats": ["Grassland", "Open Woodland", "Floodplain Edge"],
    },
    {
        "name": "Gouldian Finch",
        "scientific_name": "Erythrura gouldiae",
        "conservation_status": ConservationStatus.ENDANGERED,
        "summary": "Highly distinctive finch associated with tropical savannas and reliable water sources.",
        "habitats": ["Savanna Woodland", "Riparian Zone"],
    },
    {
        "name": "Flatback Turtle",
        "scientific_name": "Natator depressus",
        "conservation_status": ConservationStatus.VULNERABLE,
        "summary": "Marine turtle that nests on northern Australian beaches, including NT coastlines.",
        "habitats": ["Coastal Beach", "Marine Shelf"],
    },
    {
        "name": "Ghost Bat",
        "scientific_name": "Macroderma gigas",
        "conservation_status": ConservationStatus.VULNERABLE,
        "summary": "Australia's only carnivorous bat, using caves and rocky shelters across the Top End.",
        "habitats": ["Cave", "Rocky Escarpment"],
    },
]


class Command(BaseCommand):
    help = "Seed the database with authentic Northern Territory fauna and flora records."

    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0

        for raw_species_data in SPECIES_DATA:
            species_data = raw_species_data.copy()
            habitat_names = species_data.pop("habitats")
            species, created = Species.objects.update_or_create(
                scientific_name=species_data["scientific_name"],
                defaults={**species_data, "is_native_to_nt": True},
            )

            habitats = []
            for habitat_name in habitat_names:
                habitat, _ = Habitat.objects.get_or_create(name=habitat_name)
                habitats.append(habitat)

            species.habitats.set(habitats)

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"NT fauna seed complete: {created_count} created, {updated_count} updated."
            )
        )
