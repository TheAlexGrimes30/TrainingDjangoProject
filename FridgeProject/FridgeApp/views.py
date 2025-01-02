from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from FridgeApp.forms import FridgeForm, FridgeImageForm
from FridgeApp.models import Fridge, FridgeImage
from FridgeApp.utils import TitleMixin, FridgeFilterMixin, FridgeContextMixin


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

class FridgeCreateView(TitleMixin, CreateView):
    model = Fridge
    form_class = FridgeForm
    template_name = 'fridge_create.html'
    title = "Create a New Fridge"

    def form_valid(self, form):
        fridge = form.save(commit=False)
        fridge.save()
        return redirect('image-upload', slug=fridge.slug)


class FridgeListView(FridgeFilterMixin, FridgeContextMixin, TitleMixin, ListView):
    model = Fridge
    template_name = 'fridges.html'
    context_object_name = 'fridges'
    paginate_by = 7
    title = "Fridges"

    def get_queryset(self):
        queryset = Fridge.objects.all()

        queryset = self.get_filter_fridge_data(queryset)

        return queryset


class FridgeImageCreateView(TitleMixin, CreateView):
    model = FridgeImage
    form_class = FridgeImageForm
    template_name = 'image_create.html'
    title = "Upload Fridge Image"

    def form_valid(self, form):
        fridge_slug = self.kwargs['slug']
        fridge = Fridge.objects.get(slug=fridge_slug)
        form.instance.fridge = fridge
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fridge'] = Fridge.objects.get(slug=self.kwargs['slug'])
        return context

    def get_success_url(self):
        return reverse_lazy('details', kwargs={'slug': self.kwargs['slug']})

class FridgeDetailView(TitleMixin, DetailView):
    model = Fridge
    template_name = 'details.html'
    context_object_name = 'fridge'
    title = "Fridge Details"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = self.object.images.all()
        return context

class FridgeUpdateView(TitleMixin, UpdateView):
    model = Fridge
    form_class = FridgeForm
    template_name = 'update.html'
    title = "Update Fridge"

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

class FridgeDeleteView(TitleMixin, DeleteView):
    model = Fridge
    template_name = "delete.html"
    success_url = reverse_lazy('fridges')
    title = "Delete Fridge"

    def delete(self, request, *args, **kwargs):
        fridge = self.get_object()
        FridgeImage.objects.filter(fridge=fridge).delete()
        return super().delete(request, *args, **kwargs)
