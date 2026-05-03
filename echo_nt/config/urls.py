from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("echo_nt.users.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("echo_nt.observations.urls")),
    path("", include("echo_nt.fauna.urls")),
]