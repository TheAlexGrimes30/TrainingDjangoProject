from datetime import datetime, timezone, timedelta

from django.contrib import messages
from django.http import JsonResponse
import jwt
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from AuthApp.models import CustomUser
from AuthApp.forms import CustomUserRegistrationForm

class CustomUserRegistrationView(CreateView):
    model = CustomUser
    form_class = CustomUserRegistrationForm
    template_name = "register.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save(commit=False)
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()

        messages.success(self.request, "Registration successful! Please log in.")
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, "There were errors with your registration form.")
        return super().form_invalid(form)