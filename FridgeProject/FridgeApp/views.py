from django.http import HttpResponse
from django.shortcuts import render

def home(request) -> HttpResponse:
    context = {
        "title": "Home"
    }
    return render(request, "home.html", context=context)

def contacts(request) -> HttpResponse:
    context = {
        "title": "Contacts"
    }
    return render(request, "contacts.html", context=context)

def info(request) -> HttpResponse:
    context = {
        "title": "About us"
    }
    return render(request, "info.html", context=context)