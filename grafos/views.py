from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from grafos.models import Grafo, Algoritmo
from grafos.serializers import GrafoSerializers,AlgoritmoSerializers
# Create your views here.

@csrf_exempt
def grafoApi(request,id=0):
    if request.method=='GET':
        grafo= Grafo.objects.all()
        grafo_serializers=GrafoSerializers(grafo,many=True)
        return JsonResponse(grafo_serializers.data, safe=False)
    elif request.method=='POST':
        grafo_data=JSONParser().parse(request)
        grafo_serializers=GrafoSerializers(data=grafo_data)
        if grafo_serializers.is_valid():
            grafo_serializers.save()
            return JsonResponse("Se agrego con exito", safe=False)
        return JsonResponse("Fallo la insersion", safe=False)
    elif request.method=='PUT':
        grafo_data=JSONParser().parse(request)
        grafo=Grafo.objects.get(GrafoId=grafo_data['GrafoId'])
        grafo_serializers=GrafoSerializers(grafo,data=grafo_data)
        if grafo_serializers.is_valid():
            grafo_serializers.save()
            return JsonResponse("Actualizado con exito", safe=False)
        return JsonResponse("Fallo la actualizacion", safe=False)
    elif request.method=='DELETE':
        grafo=Grafo.objects.get(GrafoId=id)
        grafo.delete()
        return JsonResponse("Eliminacion con exito", safe=False)

