from rest_framework import serializers
from grafos.models import Grafo, Algoritmo, HistorialEjecutciones

class GrafoSerializers(serializers.ModelSerializer):
    class Meta:
        model=Grafo
        field=('GrafoId','NombreGrafo','nodes','links','dirigido', 'ponderado','conexo', 'multigrafo','ciclico','aciclico','bipartito','completo')
        fields = '__all__' 
class AlgoritmoSerializers(serializers.ModelSerializer):
    class Meta:
        model=Algoritmo
        field=('AlgoritmoId','NombreAlgoritmo','RutaAlgoritmo','OrdenAlgoritmo')
        fields = '__all__' 
class HistorialEjecucionesSerializers(serializers.ModelSerializer):
    class Meta:
        model=HistorialEjecutciones
        field=('HistorialId','GrafoId','AlgoritmoId','TiempoTeorico', 'TiempoReal')
        fields = '__all__' 