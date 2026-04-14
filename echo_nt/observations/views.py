from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Observation
from .forms import ObservationForm

class ObservationListView(ListView):
    model = Observation
    template_name = 'observations/observation_list.html'
    context_object_name = 'observations'

    def get_queryset(self):
        # Using QuerySet APIs: select_related for optimization (ForeignKey), prefetch_related for M2M if needed
        # excluding observations without notes as an example of exclude()
        # filter() to only show recent ones or any specific logic, here we just show all ordered by date
        return Observation.objects.select_related('user', 'species').exclude(notes__exact='').order_by('-date_spotted')

class ObservationDetailView(DetailView):
    model = Observation
    template_name = 'observations/observation_detail.html'
    context_object_name = 'observation'
    
    def get_queryset(self):
        # Optimization
        return Observation.objects.select_related('user', 'species')

class ObservationCreateView(LoginRequiredMixin, CreateView):
    model = Observation
    form_class = ObservationForm
    template_name = 'observations/observation_form.html'
    success_url = reverse_lazy('observation-list')

    # Handle business logic to auto-assign the currently logged in user
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ObservationUpdateView(LoginRequiredMixin, UpdateView):
    model = Observation
    form_class = ObservationForm
    template_name = 'observations/observation_form.html'
    success_url = reverse_lazy('observation-list')

class ObservationDeleteView(LoginRequiredMixin, DeleteView):
    model = Observation
    template_name = 'observations/observation_confirm_delete.html'
    success_url = reverse_lazy('observation-list')