from django.apps import AppConfig


class FaunaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "echo_nt.fauna"
    verbose_name = "Fauna Catalogue"

