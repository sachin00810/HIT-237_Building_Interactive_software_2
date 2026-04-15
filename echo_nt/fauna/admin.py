from django.contrib import admin

from .models import Habitat, Species


@admin.register(Habitat)
class HabitatAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ("name", "scientific_name", "conservation_status", "is_native_to_nt")
    list_filter = ("conservation_status", "is_native_to_nt")
    search_fields = ("name", "scientific_name")
    filter_horizontal = ("habitats",)

