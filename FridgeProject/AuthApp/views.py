from datetime import datetime, timezone, timedelta

from django.contrib import messages
from django.http import JsonResponse
import jwt
from django.urls import reverse_lazy
from django.views.generic import CreateView

from AuthApp.models import CustomUser
from AuthApp.forms import CustomUserRegistrationForm
from FridgeProject import settings


class CustomUserRegistrationView(CreateView):
    model = CustomUser
    form_class = CustomUserRegistrationForm
    template_name = "register.html"
    success_url = reverse_lazy("home")

    def create_jwt(self, user):
        exp_time = datetime.now(tz=timezone.utc) + timedelta(days=settings.JWT_EXP_DELTA_DAYS)

        payload = {
            'user_id': user.id,
            'username': user.username,
            'exp': exp_time,
            'iat': datetime.now(tz=timezone.utc),
        }

        token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return token

    def form_valid(self, form) -> JsonResponse:
        user = form.save(commit=False)
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()

        token = self.create_jwt(user)
        messages.success(self.request, "Registration successful! Please log in!")

        response_data = {
            'message': "Registration successful!",
            'token': token,
        }

        return JsonResponse(response_data, status=201)

    def form_invalid(self, form):
        messages.error(self.request, "There were errors with your registration form.")
        return super().form_invalid(form)

