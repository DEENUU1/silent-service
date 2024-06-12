from django.contrib.auth import login, logout
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy

from django.views.generic.edit import FormView
from dotenv import load_dotenv
from .forms import (
    RegistrationForm,
    LoginForm,
)

load_dotenv()


class RegisterUserView(FormView):
    form_class = RegistrationForm
    template_name = "user/register.html"
    success_url = reverse_lazy("warehouse:device-list")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.set_password(form.cleaned_data["password"])
        user.save()
        return super().form_valid(form)


class LoginUserView(FormView):
    template_name = "user/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("warehouse:device-list")

    def form_valid(self, form):
        """
        Overrides the parent class method to log the user in upon successful
        authentication and redirect them to the success URL.
        """
        login(self.request, form.get_user())
        return super().form_valid(form)


class LogoutUserView(LogoutView):
    def get(self, request):
        logout(request)
        return redirect("warehouse:device-list")
