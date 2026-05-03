from django.shortcuts import render
from .models import Species

def species_list(request):
    species = Species.objects.all()
    return render(request, 'species_list.html', {'species': species})