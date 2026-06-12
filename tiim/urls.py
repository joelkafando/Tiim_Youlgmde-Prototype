from django.urls import path
from . import views

urlpatterns = [
    path("", views.accueil, name="accueil"),
    path("patient/", views.patient, name="patient"),
    path("pharmacien/", views.pharmacien, name="pharmacien"),
    path("gouvernement/", views.gouvernement, name="gouvernement"),
    path("fabricant/", views.fabricant, name="fabricant"),
]
