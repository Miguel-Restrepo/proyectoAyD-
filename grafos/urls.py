
from grafos import views
from django.conf.urls import *
from django.urls import path
urlpatterns=[
    path('grafo', views.grafoApi),
    path('grafo/<int:id>',  views.grafoApi),
    path('grafo/generaraleatorio', views.grafoAleatorio),
    path('grafo/validar', views.grafoValidar)
]