from __future__ import annotations

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Prefetch


class ConservationStatus(models.TextChoices):
    LEAST_CONCERN = "LC", "Least Concern"
    NEAR_THREATENED = "NT", "Near Threatened"
    VULNERABLE = "VU", "Vulnerable"
    ENDANGERED = "EN", "Endangered"
    CRITICALLY_ENDANGERED = "CR", "Critically Endangered"

    @classmethod
    def threatened_values(cls) -> tuple[str, ...]:
        return (cls.VULNERABLE, cls.ENDANGERED, cls.CRITICALLY_ENDANGERED)


class Habitat(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class SpeciesQuerySet(models.QuerySet):
    def native_to_nt(self):
        return self.filter(is_native_to_nt=True)

    def threatened(self):
        return self.filter(
            conservation_status__in=ConservationStatus.threatened_values()
        )

    def with_habitat_details(self):
        return self.prefetch_related(
            Prefetch(
                "habitats",
                queryset=Habitat.objects.only("id", "name").order_by("name"),
            )
        )

    def ordered_for_catalogue(self):
        return self.order_by("name", "scientific_name")


class SpeciesManager(models.Manager.from_queryset(SpeciesQuerySet)):
    def get_queryset(self):
        return super().get_queryset().ordered_for_catalogue()

    def for_catalogue(self):
        return self.get_queryset().with_habitat_details()


class NTNativeSpeciesManager(SpeciesManager):
    def get_queryset(self):
        return super().get_queryset().native_to_nt()


class Species(models.Model):
    name = models.CharField(max_length=120, db_index=True)
    scientific_name = models.CharField(max_length=160, unique=True)
    conservation_status = models.CharField(
        max_length=2,
        choices=ConservationStatus.choices,
        default=ConservationStatus.LEAST_CONCERN,
        db_index=True,
    )
    summary = models.TextField(blank=True)
    is_native_to_nt = models.BooleanField(default=False, db_index=True)
    habitats = models.ManyToManyField(Habitat, related_name="species", blank=True)

    objects = SpeciesManager()
    native_species = NTNativeSpeciesManager()

    class Meta:
        ordering = ("name", "scientific_name")
        indexes = [
            models.Index(
                fields=["is_native_to_nt", "conservation_status"],
                name="species_nt_status_idx",
            ),
        ]

    def __str__(self) -> str:
        return self.display_name

    @property
    def display_name(self) -> str:
        return f"{self.name} ({self.scientific_name})"

    @property
    def is_threatened(self) -> bool:
        return self.conservation_status in ConservationStatus.threatened_values()

    def clean(self):
        self.name = self.name.strip()
        self.scientific_name = self.scientific_name.strip()
        self.summary = self.summary.strip()

        if not self.name:
            raise ValidationError({"name": "Common name cannot be blank."})
        if not self.scientific_name:
            raise ValidationError(
                {"scientific_name": "Scientific name cannot be blank."}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def change_conservation_status(self, new_status: str, *, save: bool = True):
        self.conservation_status = new_status
        if save:
            self.save(update_fields=["conservation_status"])

    def update_summary(self, new_summary: str, *, save: bool = True):
        self.summary = new_summary.strip()
        if save:
            self.save(update_fields=["summary"])

    def mark_as_nt_native(self, *, save: bool = True):
        self.is_native_to_nt = True
        if save:
            self.save(update_fields=["is_native_to_nt"])

    def assign_habitats(self, *habitats: Habitat):
        if self.pk is None:
            raise ValueError("Species must be saved before habitats can be assigned.")

        self.habitats.set(habitats)
