from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ("viewer", "Viewer"),
        ("ranger", "Ranger"),
        ("researcher", "Researcher"),
    )
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default="viewer"
    )

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
