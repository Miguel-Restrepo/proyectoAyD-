from rest_framework import serializers
from grafos.models import Grafo, Algoritmo

class GrafoSerializers(serializers.ModelSerializer):
    class Meta:
        model=Grafo
        field=('GrafoId','NombreGrafo','nodes','links','dirigido', 'ponderado','conexo', 'multigrafo','ciclico','aciclico','bipartito','completo')
        fields = '__all__' 
class AlgoritmoSerializers(serializers.ModelSerializer):
    class Meta:
        model=Algoritmo
        field=('AlgoritmoId','NombreAlgoritmo','RutaAlgoritmo','OrdenAlgoritmo')