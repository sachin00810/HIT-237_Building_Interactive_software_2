from __future__ import annotations

from datetime import timedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.text import Truncator

from echo_nt.fauna.models import Species


class Observation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="observations",
    )
    species = models.ForeignKey(
        Species,
        on_delete=models.PROTECT,
        related_name="observations",
    )
    notes = models.TextField(blank=True)
    date_spotted = models.DateTimeField(default=timezone.now, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-date_spotted",)
        indexes = [
            models.Index(fields=["user", "date_spotted"], name="obs_user_date_idx"),
            models.Index(
                fields=["species", "date_spotted"],
                name="obs_species_date_idx",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.species.name} observed by {self.user} on {self.date_spotted:%Y-%m-%d %H:%M}"

    @property
    def cleaned_notes(self) -> str:
        return self.notes.strip()

    @property
    def notes_excerpt(self) -> str:
        if not self.cleaned_notes:
            return "No field notes recorded."
        return Truncator(self.cleaned_notes).chars(80)

    @property
    def is_recent_sighting(self) -> bool:
        return self.date_spotted >= timezone.now() - timedelta(hours=24)

    def clean(self):
        self.notes = self.notes.strip()
        if self.date_spotted and self.date_spotted > timezone.now():
            raise ValidationError(
                {"date_spotted": "Observation date cannot be in the future."}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
