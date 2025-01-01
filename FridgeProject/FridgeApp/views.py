from django.http import HttpResponse
from django.shortcuts import render
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView

from FridgeApp.forms import FridgeForm, FridgeImageForm
from FridgeApp.models import Fridge, FridgeImage


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

class FridgeCreateView(CreateView):
    model = Fridge
    form_class = FridgeForm
    template_name = 'fridge_create.html'
    success_url = reverse_lazy('fridges')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create a New Fridge'
        return context

class FridgeListView(ListView):
    model = Fridge
    template_name = 'fridges.html'
    context_object_name = 'fridges'

    def get_queryset(self):
        queryset = Fridge.objects.all()

        brand = self.request.GET.get('brand')
        model = self.request.GET.get('model')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        min_capacity = self.request.GET.get('min_capacity')
        max_capacity = self.request.GET.get('max_capacity')

        if brand:
            queryset = queryset.filter(brand__icontains=brand)

        if model:
            queryset = queryset.filter(model__icontains=model)

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        if min_capacity:
            queryset = queryset.filter(capacity__gte=min_capacity)

        if max_capacity:
            queryset = queryset.filter(capacity__lte=max_capacity)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filters'] = {
            'brand': self.request.GET.get('brand', ''),
            'model': self.request.GET.get('model', ''),
            'min_price': self.request.GET.get('min_price', ''),
            'max_price': self.request.GET.get('max_price', ''),
            'min_capacity': self.request.GET.get('min_capacity', ''),
            'max_capacity': self.request.GET.get('max_capacity', ''),
        }
        return context

class FridgeImageCreateView(CreateView):
    model = FridgeImage
    form_class = FridgeImageForm
    template_name = 'image_create.html'

