# backend/api/urls.py
from django.urls import path
from .views import checkout, inbound

urlpatterns = [
    path("checkout", checkout),
    path("inbound", inbound),
]