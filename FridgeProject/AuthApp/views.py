from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from AuthApp.models import CustomUser
from AuthApp.forms import CustomUserRegistrationForm, LoginForm


class CustomUserRegistrationView(CreateView):
    model = CustomUser
    form_class = CustomUserRegistrationForm
    template_name = "register.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()

        messages.success(self.request, "Registration successful! Please log in.")
        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(self.request, "There were errors with your registration form.")
        return super().form_invalid(form)

class CustomLoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def get_success_url(self) -> HttpResponseRedirect:
        return reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        try:
            user = CustomUser.objects.get(username=username)

            if user.check_password(password):
                login(self.request, user)
                messages.success(self.request, "You have successfully logged in!")
                return redirect(self.get_success_url())
            else:
                messages.error(self.request, "Invalid password")
                return self.form_invalid(form)
        except CustomUser.DoesNotExist:
            messages.error(self.request, "User does not exist")
            return self.form_invalid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

