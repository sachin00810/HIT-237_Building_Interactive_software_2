from __future__ import annotations

from django.core.management.base import BaseCommand
from django.db import transaction

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
        "summary": "Carnivorous marsupial under pressure from cane toads, intense fires, and habitat decline.",
        "habitats": ["Savanna Woodland", "Rocky Escarpment"],
    },
    {
        "name": "Red Kangaroo",
        "scientific_name": "Osphranter rufus",
        "conservation_status": ConservationStatus.LEAST_CONCERN,
        "summary": "Australia's largest marsupial, widespread across the arid and semi-arid NT interior.",
        "habitats": ["Desert Plain", "Grassland"],
    },
    {
        "name": "Brolga",
        "scientific_name": "Antigone rubicunda",
        "conservation_status": ConservationStatus.LEAST_CONCERN,
        "summary": "Tall wetland crane famous for elaborate pair dancing displays on northern floodplains.",
        "habitats": ["Wetland", "Floodplain"],
    },
    {
        "name": "Kakadu Plum",
        "scientific_name": "Terminalia ferdinandiana",
        "conservation_status": ConservationStatus.LEAST_CONCERN,
        "summary": "Iconic native NT tree valued for nutrient-rich fruit and strong cultural significance.",
        "habitats": ["Open Woodland", "Floodplain Edge"],
    },
    {
        "name": "Black-footed Tree-rat",
        "scientific_name": "Mesembriomys gouldii",
        "conservation_status": ConservationStatus.ENDANGERED,
        "summary": "Large arboreal rodent persisting in fragmented patches of savanna and monsoon forest.",
        "habitats": ["Monsoon Forest", "Savanna Woodland"],
    },
    {
        "name": "Greater Bilby",
        "scientific_name": "Macrotis lagotis",
        "conservation_status": ConservationStatus.VULNERABLE,
        "summary": "Nocturnal digging marsupial still recorded in parts of the Tanami and central deserts.",
        "habitats": ["Desert Plain", "Spinifex Grassland"],
    },
    {
        "name": "Emu",
        "scientific_name": "Dromaius novaehollandiae",
        "conservation_status": ConservationStatus.LEAST_CONCERN,
        "summary": "Large flightless bird that tracks seasonal food and water resources across open country.",
        "habitats": ["Grassland", "Open Woodland"],
    },
    {
        "name": "Agile Wallaby",
        "scientific_name": "Notamacropus agilis",
        "conservation_status": ConservationStatus.LEAST_CONCERN,
        "summary": "Common Top End wallaby seen in grasslands, woodlands, and floodplain margins.",
        "habitats": ["Grassland", "Open Woodland", "Floodplain Edge"],
    },
    {
        "name": "Gouldian Finch",
        "scientific_name": "Erythrura gouldiae",
        "conservation_status": ConservationStatus.ENDANGERED,
        "summary": "Highly distinctive finch associated with tropical savannas and reliable dry-season water.",
        "habitats": ["Savanna Woodland", "Riparian Zone"],
    },
    {
        "name": "Flatback Turtle",
        "scientific_name": "Natator depressus",
        "conservation_status": ConservationStatus.VULNERABLE,
        "summary": "Marine turtle nesting on northern Australian beaches, including remote NT coastlines.",
        "habitats": ["Coastal Beach", "Marine Shelf"],
    },
    {
        "name": "Ghost Bat",
        "scientific_name": "Macroderma gigas",
        "conservation_status": ConservationStatus.VULNERABLE,
        "summary": "Australia's only carnivorous bat, sheltering in caves and rocky escarpments.",
        "habitats": ["Cave", "Rocky Escarpment"],
    },
    {
        "name": "Frill-necked Lizard",
        "scientific_name": "Chlamydosaurus kingii",
        "conservation_status": ConservationStatus.LEAST_CONCERN,
        "summary": "Distinctive reptile of northern woodlands, famous for its dramatic defensive frill display.",
        "habitats": ["Savanna Woodland", "Monsoon Forest Edge"],
    },
    {
        "name": "Olive Python",
        "scientific_name": "Liasis olivaceus",
        "conservation_status": ConservationStatus.LEAST_CONCERN,
        "summary": "Large python found near rivers, gorges, and rocky landscapes in northern Australia.",
        "habitats": ["River", "Rocky Gorge"],
    },
    {
        "name": "Northern Brushtail Possum",
        "scientific_name": "Trichosurus arnhemensis",
        "conservation_status": ConservationStatus.LEAST_CONCERN,
        "summary": "Nocturnal possum native to the Top End, commonly associated with wooded habitats.",
        "habitats": ["Monsoon Forest", "Open Woodland"],
    },
]


class Command(BaseCommand):
    help = "Bulk seed authentic Northern Territory species and habitat relationships."

    def add_arguments(self, parser):
        parser.add_argument(
            "--refresh",
            action="store_true",
            help="Update existing species summaries and conservation details on reruns.",
        )
        parser.add_argument(
            "--batch-size",
            type=int,
            default=100,
            help="Batch size used for bulk_create and bulk_update operations.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        batch_size = options["batch_size"]
        refresh = options["refresh"]

        habitat_names = sorted(
            {habitat for species in SPECIES_DATA for habitat in species["habitats"]}
        )
        existing_habitats = Habitat.objects.in_bulk(habitat_names, field_name="name")
        habitats_to_create = [
            Habitat(name=name) for name in habitat_names if name not in existing_habitats
        ]

        Habitat.objects.bulk_create(
            habitats_to_create,
            batch_size=batch_size,
            ignore_conflicts=True,
        )
        habitats_by_name = Habitat.objects.in_bulk(habitat_names, field_name="name")

        scientific_names = [item["scientific_name"] for item in SPECIES_DATA]
        existing_species = Species.objects.in_bulk(
            scientific_names,
            field_name="scientific_name",
        )

        species_to_create = []
        species_to_update = []

        for item in SPECIES_DATA:
            species = existing_species.get(item["scientific_name"])
            if species is None:
                species_to_create.append(
                    Species(
                        name=item["name"],
                        scientific_name=item["scientific_name"],
                        conservation_status=item["conservation_status"],
                        summary=item["summary"],
                        is_native_to_nt=True,
                    )
                )
                continue

            if not refresh:
                continue

            has_changed = False
            for field in ("name", "conservation_status", "summary"):
                new_value = item[field]
                if getattr(species, field) != new_value:
                    setattr(species, field, new_value)
                    has_changed = True

            if not species.is_native_to_nt:
                species.is_native_to_nt = True
                has_changed = True

            if has_changed:
                species_to_update.append(species)

        Species.objects.bulk_create(
            species_to_create,
            batch_size=batch_size,
            ignore_conflicts=True,
        )

        if species_to_update:
            Species.objects.bulk_update(
                species_to_update,
                ["name", "conservation_status", "summary", "is_native_to_nt"],
                batch_size=batch_size,
            )

        seeded_species = Species.objects.filter(
            scientific_name__in=scientific_names
        ).in_bulk(field_name="scientific_name")

        through_model = Species.habitats.through
        if refresh:
            through_model.objects.filter(
                species_id__in=[
                    seeded_species[item["scientific_name"]].id for item in SPECIES_DATA
                ]
            ).delete()

        habitat_links = []
        for item in SPECIES_DATA:
            species = seeded_species[item["scientific_name"]]
            for habitat_name in item["habitats"]:
                habitat_links.append(
                    through_model(
                        species_id=species.id,
                        habitat_id=habitats_by_name[habitat_name].id,
                    )
                )

        through_model.objects.bulk_create(
            habitat_links,
            batch_size=batch_size,
            ignore_conflicts=True,
        )

        self.stdout.write(
            self.style.SUCCESS(
                "NT fauna seed complete: "
                f"{len(species_to_create)} species created, "
                f"{len(species_to_update)} species refreshed, "
                f"{len(habitats_to_create)} habitats created, "
                f"{len(SPECIES_DATA)} catalogue records synced."
            )
        )

        if not refresh:
            self.stdout.write(
                self.style.WARNING(
                    "Run the command again with --refresh to overwrite existing "
                    "species summaries, statuses, and habitat links."
                )
            )
