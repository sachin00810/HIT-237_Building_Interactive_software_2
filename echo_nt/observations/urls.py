from django.urls import path
from .views import (
    ObservationListView,
    ObservationDetailView,
    ObservationCreateView,
    ObservationUpdateView,
    ObservationDeleteView
)

urlpatterns = [
    path('', ObservationListView.as_view(), name='observation-list'),
    path('observation/<int:pk>/', ObservationDetailView.as_view(), name='observation-detail'),
    path('observation/new/', ObservationCreateView.as_view(), name='observation-create'),
    path('observation/<int:pk>/update/', ObservationUpdateView.as_view(), name='observation-update'),
    path('observation/<int:pk>/delete/', ObservationDeleteView.as_view(), name='observation-delete'),
]