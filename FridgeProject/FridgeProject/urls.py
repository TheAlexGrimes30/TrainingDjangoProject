"""
URL configuration for FridgeProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from FridgeApp.views import home, contacts, info, FridgeCreateView, FridgeListView, FridgeImageCreateView, \
    FridgeDetailView
from FridgeProject import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('contacts/', contacts, name="contacts"),
    path('info/', info, name="info"),
    path('create/', FridgeCreateView.as_view(), name="create"),
    path('fridges/', FridgeListView.as_view(), name="fridges"),
    path('create/<slug:slug>/image-upload/', FridgeImageCreateView.as_view(), name="image-upload"),
    path('fridges/<slug:slug>/', FridgeDetailView.as_view(), name='details'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
