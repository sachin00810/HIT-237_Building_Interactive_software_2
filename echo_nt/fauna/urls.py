from django.urls import path
from .views import species_list

urlpatterns = [
    path("species/", species_list, name="species-list"),
]