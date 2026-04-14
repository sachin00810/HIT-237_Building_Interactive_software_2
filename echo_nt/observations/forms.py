from django import forms
from .models import Observation

class ObservationForm(forms.ModelForm):
    class Meta:
        model = Observation
        fields = ['species', 'notes']
        widgets = {
            'species': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter observation notes...'}),
        }
