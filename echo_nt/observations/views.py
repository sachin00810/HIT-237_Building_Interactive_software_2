from __future__ import annotations

from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Prefetch
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from echo_nt.fauna.models import Habitat

from .forms import ObservationForm
from .models import Observation


class ObservationQuerysetMixin:
    queryset = Observation.objects.select_related("user", "species").prefetch_related(
        Prefetch(
            "species__habitats",
            queryset=Habitat.objects.only("id", "name").order_by("name"),
        )
    )

    def get_queryset(self):
        return self.queryset


class AuthorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    raise_exception = True
    permission_denied_message = "You can only modify your own observations."

    def test_func(self):
        return self.get_object().user_id == self.request.user.id

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied(self.permission_denied_message)
        return super().handle_no_permission()


class ObservationListView(ObservationQuerysetMixin, ListView):
    model = Observation
    template_name = "observations/observation_list.html"
    context_object_name = "observations"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().exclude(notes__exact="")
        species_id = self.request.GET.get("species")
        scope = self.request.GET.get("scope")
        window = self.request.GET.get("window")

        if species_id and species_id.isdigit():
            queryset = queryset.filter(species_id=int(species_id))
        if scope == "mine" and self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)
        if window == "recent":
            queryset = queryset.filter(
                date_spotted__gte=timezone.now() - timedelta(hours=24)
            )

        return queryset.order_by("-date_spotted", "species__name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_scope"] = self.request.GET.get("scope", "all")
        context["active_window"] = self.request.GET.get("window", "all")
        context["selected_species_id"] = self.request.GET.get("species", "")
        return context


class ObservationDetailView(ObservationQuerysetMixin, DetailView):
    model = Observation
    template_name = "observations/observation_detail.html"
    context_object_name = "observation"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_edit"] = (
            self.request.user.is_authenticated
            and self.object.user_id == self.request.user.id
        )
        return context


class ObservationCreateView(LoginRequiredMixin, CreateView):
    model = Observation
    form_class = ObservationForm
    template_name = "observations/observation_form.html"

    def get_initial(self):
        initial = super().get_initial()
        species_id = self.request.GET.get("species")
        if species_id and species_id.isdigit():
            initial["species"] = int(species_id)
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("observation-detail", kwargs={"pk": self.object.pk})


class ObservationUpdateView(
    AuthorRequiredMixin, ObservationQuerysetMixin, UpdateView
):
    model = Observation
    form_class = ObservationForm
    template_name = "observations/observation_form.html"

    def get_success_url(self):
        return reverse("observation-detail", kwargs={"pk": self.object.pk})


class ObservationDeleteView(
    AuthorRequiredMixin, ObservationQuerysetMixin, DeleteView
):
    model = Observation
    template_name = "observations/observation_confirm_delete.html"
    success_url = reverse_lazy("observation-list")
