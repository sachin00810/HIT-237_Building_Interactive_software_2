from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import path

from .views import EchoNTLoginView, SignUpView


urlpatterns = [
    path("accounts/login/", EchoNTLoginView.as_view(), name="login"),
    path("accounts/signup/", SignUpView.as_view(), name="signup"),

    # Explicitly owned password-change URLs — these override Django's defaults
    # included via accounts/ in config/urls.py, making the auth architecture
    # fully self-contained and traceable in this app's URL configuration.
    path(
        "accounts/password-change/",
        PasswordChangeView.as_view(
            template_name="registration/password_change_form.html",
        ),
        name="password_change",
    ),
    path(
        "accounts/password-change/done/",
        PasswordChangeDoneView.as_view(
            template_name="registration/password_change_done.html",
        ),
        name="password_change_done",
    ),
]
