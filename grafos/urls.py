
from grafos import views
from django.conf.urls import *
from django.urls import path
urlpatterns=[
    path('grafo', views.grafoApi),
    path('grafo/<int:id>',  views.grafoApi),
    path('grafo/generaraleatorio', views.grafoAleatorio),
    path('grafo/validar', views.grafoValidar),
    path('matrizadyacencia/<int:id>', views.MatrizAdyacencia),
    path('q_clustering/<int:id>', views.AlgoritmoQ_Clustering),
    path('queyranne/<int:id>', views.AlgoritmoQueyranne),
    path('mssf/<int:id>', views.AlgoritmoMssf)
]