from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.utils.crypto import get_random_string
from grafos.models import Grafo, Algoritmo
import random
from grafos.serializers import GrafoSerializers,AlgoritmoSerializers
# Create your views here.

@csrf_exempt
def grafoApi(request,id=0):
    if request.method=='GET' and id!=0:
        grafo= Grafo.objects.filter(GrafoId=id)
        grafo_serializers=GrafoSerializers(grafo,many=True)
        return JsonResponse(grafo_serializers.data[0], safe=False)
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

def grafoAleatorio(request,id=0):
    if request.method=='GET':
        dirigido = random.randint(0,1)
        ponderado = random.randint(0,1)
        conexo = random.randint(0,1)
        multigrafo = random.randint(0,1)
        ciclico= random.randint(0,1)
        aciclico=random.randint(0,1)
        if ciclico==1:
            aciclico=0
        bipartito= random.randint(0,1)
        completo= random.randint(0,1)
        if completo==1:
            bipartito=0
       
        nombre = get_random_string(length=5, allowed_chars='AEIOUJM')
        grafo=generarGrafo(nombre,dirigido,ponderado,conexo,multigrafo,ciclico,aciclico,bipartito,completo)
        #grafo_serializers=GrafoSerializers(data=grafo)
        #if grafo_serializers.is_valid():
         #   grafo_serializers.save()
        return JsonResponse(grafo, safe=False)

def grafoValidar(request):
    if request.method=='GET':
        #grafo_data=JSONParser().parse(request)
        #grafo_serializers=GrafoSerializers(data=grafo_data)
        #return JsonResponse(grafo_serializers, safe=False)
        grafo= Grafo.objects.all()
        grafo_serializers=GrafoSerializers(grafo,many=True)
        return JsonResponse(grafo_serializers.data, safe=False)

def generarGrafo(nombre,dirigido,ponderado,conexo,multigrafo,ciclico,aciclico,bipartito,completo):
    numeroNodos = random.randint(2,10) 
    nodos=[]
    for i in range(1,numeroNodos):
        pesonodo = random.randint(5,20)
        nodos.append( { 
                "id": i,
                "name": "nombre{}".format(i),
                "val": pesonodo
                })
       
    numeroAristas=0
    aristas=[]
    if dirigido==0:
        numeroAristas = random.randint(numeroNodos-1,numeroNodos*2)
    else:
        numeroAristas = random.randint(numeroNodos-1,numeroNodos*2+numeroNodos)
    for i in range(1,numeroAristas):
        pesoArista = random.randint(5,20)
        nodoOrigen= random.randint(1,numeroNodos)
        nodoDestino= random.randint(1,numeroNodos)
        if nodoOrigen==nodoDestino:
            aristas.append( {
                    "source": nodoOrigen,
                    "target": nodoDestino,
                    "curvature": 1, 
                    "rotation": 0,
                    "weight": pesoArista 
                } )
        else:
            aristas.append( {
                        "source": nodoOrigen,
                        "target": nodoDestino,
                        "weight": pesoArista
                    })
    grafo= {
            "NombreGrafo":nombre,
            "nodes": nodos,
            "links": aristas,
            "Dirigido":dirigido,
            "Ponderado":ponderado,
            "Conexo":conexo,
            "Multigrafo" : multigrafo,
            "Ciclico": ciclico,
            "Aciclico": aciclico,
            "Bipartito":bipartito,
            "Completo":completo
        }
    return grafo
def generarNodosyAristas(conexo):

    if conexo==1 and not(verificarConexo()):
        generarNodosyAristas(conexo)
    return []
def verificarConexo(nodos,aristas):
    return True
def verificarDirigido():
    return True
def verificarMultigrafo():
    return True
def verificarCiclico():
    return True
def verificarAciclico():
    return True
def verificarBipartito():
    return True
def verificarCompleto():
    return True
def verificarPonderado():
    return True