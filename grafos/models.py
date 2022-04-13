from django.db import models

# Create your models here.
class Grafo(models.Model):
    GrafoId = models.AutoField(primary_key=True)
    NombreGrafo= models.CharField(max_length=500)
class Algoritmo(models.Model):
    AlgoritmoId = models.AutoField(primary_key=True)
    NombreAlgoritmo= models.CharField(max_length=500)
    RutaAlgoritmo= models.CharField(max_length=500)
    OrdenAlgoritmo= models.CharField(max_length=500)
