from django.contrib import admin

from .models import Observation


@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    list_display = ("species", "user", "date_spotted", "created_at")
    list_filter = ("date_spotted", "species")
    search_fields = ("species__name", "user__username", "notes")
    autocomplete_fields = ("species", "user")

