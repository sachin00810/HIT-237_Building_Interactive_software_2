from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import EmailOrUsernameAuthenticationForm, SignUpForm


class EchoNTLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = EmailOrUsernameAuthenticationForm
    redirect_authenticated_user = True


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("observation-list")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(
            self.request,
            "Your account has been created and you are now signed in.",
        )
        return response
