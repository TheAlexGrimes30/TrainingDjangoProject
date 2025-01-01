from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView

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

    def form_valid(self, form):
        fridge = form.save(commit=False)
        fridge.save()
        return redirect('image-upload', slug=fridge.slug)

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

    def form_valid(self, form):
        fridge_slug = self.kwargs['slug']
        fridge = Fridge.objects.get(slug=fridge_slug)
        form.instance.fridge = fridge
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'New Fridge Image'
        context['fridge'] = Fridge.objects.get(slug=self.kwargs['slug'])
        return context

    def get_success_url(self):
        return reverse_lazy('details', kwargs={'slug': self.kwargs['slug']})

class FridgeDetailView(DetailView):
    model = Fridge
    template_name = 'details.html'
    context_object_name = 'fridge'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = self.object.images.all()
        return context

class FridgeUpdateView(UpdateView):
    model = Fridge
    form_class = FridgeForm
    template_name = 'update.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Fridge, slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fridge = self.get_object()
        context['fridge_image_form'] = FridgeImageForm()
        context['fridge'] = fridge
        return context

    def form_valid(self, form):
        fridge = form.save(commit=False)

        if self.request.FILES.get('image'):
            fridge_image = FridgeImage(fridge=fridge, image=self.request.FILES['image'])
            fridge_image.save()
        fridge.save()

        return redirect(reverse_lazy('details', kwargs={'slug': fridge.slug}))

    def success_url(self):
        return reverse_lazy('details', kwargs={'slug': self.kwargs['slug']})