from rest_framework import serializers
from grafos.models import Grafo, Algoritmo

class GrafoSerializers(serializers.ModelSerializer):
    class Meta:
        model=Grafo
        field=('GrafoId','NombreGrafo')
class AlgoritmoSerializers(serializers.ModelSerializer):
    class Meta:
        model=Algoritmo
        field=('AlgoritmoId','NombreAlgoritmo','RutaAlgoritmo','OrdenAlgoritmo')