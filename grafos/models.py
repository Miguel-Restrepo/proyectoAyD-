from django.db import models

# Create your models here.
class Grafo(models.Model):
    GrafoId = models.AutoField(primary_key=True)
    NombreGrafo= models.CharField(max_length=500)
    nodes=models.JSONField()
    links=models.JSONField()
    Dirigido=models.IntegerField()
    Ponderado=models.IntegerField()
    Conexo=models.IntegerField()
    Multigrafo=models.IntegerField()
    Ciclico=models.IntegerField()
    Aciclico=models.IntegerField()
    Bipartito=models.IntegerField()
    Completo=models.IntegerField()
    
class Algoritmo(models.Model):
    AlgoritmoId = models.AutoField(primary_key=True)
    NombreAlgoritmo= models.CharField(max_length=500)
    RutaAlgoritmo= models.CharField(max_length=500)
    OrdenAlgoritmo= models.CharField(max_length=500)
class HistorialEjecutciones(models.Model):
    HistorialId = models.AutoField(primary_key=True)
    GrafoId=models.IntegerField()
    AlgoritmoId=models.IntegerField()
    TiempoTeorico=models.IntegerField()
    TiempoReal=models.IntegerField()
