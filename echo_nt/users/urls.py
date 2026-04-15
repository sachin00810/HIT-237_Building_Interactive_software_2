from django.urls import path

from .views import EchoNTLoginView, SignUpView


urlpatterns = [
    path("accounts/login/", EchoNTLoginView.as_view(), name="login"),
    path("accounts/signup/", SignUpView.as_view(), name="signup"),
]
