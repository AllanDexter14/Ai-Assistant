from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("ask/", views.ask, name="ask"),
    path("service-worker.js", views.service_worker, name="service_worker"),
]