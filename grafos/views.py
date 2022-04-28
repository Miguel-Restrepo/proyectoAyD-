from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.utils.crypto import get_random_string
from grafos.models import Grafo, Algoritmo
import random
from random import choice
from grafos.serializers import GrafoSerializers, AlgoritmoSerializers
#from modelos.grafo import *

# Create your views here.


@csrf_exempt
def grafoApi(request, id=0):
    if request.method == 'GET' and id != 0:# retorna el grafo con el id indicado
        grafo = Grafo.objects.filter(GrafoId=id)
        grafo_serializers = GrafoSerializers(grafo, many=True)
        return JsonResponse(grafo_serializers.data[0], safe=False)
    if request.method == 'GET':# me retorna todos los grafos existentes en la base de datos
        grafo = Grafo.objects.all()
        grafo_serializers = GrafoSerializers(grafo, many=True)
        return JsonResponse(grafo_serializers.data, safe=False)
    elif request.method == 'POST':#me guarda un grafo
        grafo_data = JSONParser().parse(request)
        grafo_serializers = GrafoSerializers(data=grafo_data)
        if grafo_serializers.is_valid():
            grafo_serializers.save()
            return JsonResponse("Se agrego con exito", safe=False)
        return JsonResponse("Fallo la insersion", safe=False)
    elif request.method == 'PUT':#Me actualiza un grafo existente
        grafo_data = JSONParser().parse(request)
        grafo = Grafo.objects.get(GrafoId=grafo_data['GrafoId'])
        grafo_serializers = GrafoSerializers(grafo, data=grafo_data)
        if grafo_serializers.is_valid():
            grafo_serializers.save()
            return JsonResponse("Actualizado con exito", safe=False)
        return JsonResponse("Fallo la actualizacion", safe=False)
    elif request.method == 'DELETE':#Me elimina un grafo con un id especifico
        grafo = Grafo.objects.get(GrafoId=id)
        grafo.delete()
        return JsonResponse("Eliminacion con exito", safe=False)


def grafoAleatorio(request, id=0):
    if request.method == 'GET':#Me genera un grafo completamente aleatorio
        dirigido = random.randint(0, 1)
        ponderado = random.randint(0, 1)
        conexo = random.randint(0, 1)
        multigrafo = random.randint(0, 1)
        ciclico = random.randint(0, 1)
        aciclico = random.randint(0, 1)
        if ciclico == 1:
            aciclico = 0
        bipartito = random.randint(0, 1)
        completo = random.randint(0, 1)
        if completo == 1:
            bipartito = 0
        numeroNodos = random.randint(2, 15)
        numeroAristas = random.randint(
            numeroNodos-1, numeroNodos*2+numeroNodos)
        nombre = get_random_string(length=5, allowed_chars='AEIOUJM')
        grafo = generarGrafo(nombre, numeroNodos, numeroAristas, dirigido,
                             ponderado, conexo, multigrafo, ciclico, aciclico, bipartito, completo)
        # grafo_serializers=GrafoSerializers(data=grafo)
        # if grafo_serializers.is_valid():
        #   grafo_serializers.save()
        return JsonResponse(grafo, safe=False)
    elif request.method == 'POST':#Me crea  un grafo de forma aleatoria apartir de unos parametros
        grafo_data = JSONParser().parse(request)
        grafo_serializers = GrafoSerializers(data=grafo_data)
        if grafo_serializers.is_valid():
            dirigido = grafo_serializers["Dirigido"]
            ponderado = grafo_serializers["Ponderado"]
            conexo = grafo_serializers["Conexo"]
            multigrafo = grafo_serializers["Multigrafo"]
            ciclico = grafo_serializers["Ciclico"]
            aciclico = grafo_serializers["Aciclico"]
            if ciclico == 1:
                aciclico = 0
            bipartito = grafo_serializers["Bipartito"]
            completo = grafo_serializers["Completo"]
            if completo == 1:
                bipartito = 0
            numeroNodos = random.randint(2, 10)
            numeroAristas = random.randint(
                numeroNodos-1, numeroNodos*2+numeroNodos)
            nombre = get_random_string(length=5, allowed_chars='AEIOUJM')
            grafo = generarGrafo(nombre, numeroNodos, numeroAristas, dirigido,
                                 ponderado, conexo, multigrafo, ciclico, aciclico, bipartito, completo)
            # grafo_serializers=GrafoSerializers(data=grafo)
            # if grafo_serializers.is_valid():
            #   grafo_serializers.save()
            return JsonResponse(grafo, safe=False)
        return JsonResponse("Fallo", safe=False)


def grafoValidar(request):
    if request.method == 'POST':#Me valida que un grafo cumpla con los parametros
        grafo_data = JSONParser().parse(request)
        grafo_serializers = GrafoSerializers(data=grafo_data)
        if grafo_serializers.is_valid():
           # grafo_serializers.save()
            return JsonResponse("Se Valido con exito", safe=False)
        return JsonResponse("NO cumple con los parametros establecidos", safe=False)


def generarGrafo(nombre, numeroNodos, numeroAristas, dirigido, ponderado, conexo, multigrafo, ciclico, aciclico, bipartito, completo):
    nodos = []
    for i in range(1, numeroNodos):
        pesonodo = random.randint(5, 20)
        if ponderado == 1:
            nodos.append({
                "id": i,
                "name": "nombre{}".format(i),
                "val": pesonodo
            })
        else:
            nodos.append({
                "id": i,
                "name": "nombre{}".format(i)
            })
    aristas = []
    if completo == 1:
        aristas = generarCompleto(nodos, ponderado)

    elif conexo == 1:
        aristas = generarAristasConexasRecursivoNoDirigido(
            nodos, [], 1, [], ponderado)
        faltantes = buscarInaccesiblesNoDirigido(nodos, aristas)
        aristas = generarAristasFaltantes(
            faltantes, [], aristas, len(nodos), ponderado)
        if dirigido == 1:
            aristas = generarAristasConexasRecursivoDirigido(
                nodos, aristas, ponderado)
        if multigrafo == 1:
            aristas = generarMultigrafo(aristas, ponderado)
        else:
            aristas = eliminarMultigrafo(aristas)
    else:
        aristas = generarNoConexo(len(nodos), numeroAristas, ponderado)

    grafo = {
        "NombreGrafo": nombre,
        "nodes": nodos,
        "links": aristas,
        "Dirigido": dirigido,
        "Ponderado": ponderado,
        "Conexo": conexo,
        "Multigrafo": multigrafo,
        "Ciclico": ciclico,
        "Aciclico": aciclico,
        "Bipartito": bipartito,
        "Completo": completo
    }
    return grafo


def generarCompleto(listaNodos: list, ponderado):
    listaAristas = []
    for i in listaNodos:
        for j in listaNodos:
            if i != j:
                if ponderado == 1:
                    pesoArista = random.randint(5, 20)
                    listaAristas.append({
                        "source": i["id"],
                        "target": j["id"],
                        "weight": pesoArista,
                        "curvature": random.random(), 
                        "rotation": 0
                    })
                else:
                    listaAristas.append({
                        "source": i["id"],
                        "target": j["id"],
                        "curvature": random.random(), 
                        "rotation": 0
                    })
    return listaAristas


def generarNoConexo(numeroNodos, numeroAristas, ponderado):
    aristas = []
    for i in range(1, numeroAristas):

        nodoOrigen = random.randint(1, numeroNodos)
        nodoDestino = random.randint(1, numeroNodos)
        if ponderado == 1:
            pesoArista = random.randint(5, 20)
            if nodoOrigen == nodoDestino:
                aristas.append({
                    "source": nodoOrigen,
                    "target": nodoDestino,
                    "curvature": random.random(),
                    "rotation": 0,
                    "weight": pesoArista
                })
            else:
                aristas.append({
                    "source": nodoOrigen,
                    "target": nodoDestino,
                    "weight": pesoArista,
                    "curvature": random.random(),
                    "rotation": 0
                })
        else:
            if nodoOrigen == nodoDestino:
                aristas.append({
                    "source": nodoOrigen,
                    "target": nodoDestino,
                    "curvature": random.random(),
                    "rotation": 0
                })
            else:
                aristas.append({
                    "source": nodoOrigen,
                    "target": nodoDestino,
                    "curvature": random.random(), 
                        "rotation": 0
                })
    return aristas


def generarAristasConexasRecursivoNoDirigido(listaNodos, nodosVisitados: list, nodoVoy, listaAristas: list, ponderado):
    if len(nodosVisitados) == len(listaNodos) or nodoVoy > len(listaNodos):
        return listaAristas
    pesoArista = random.randint(5, 20)
    nodoOrigen = nodoVoy
    nodoDestino = generarNuevo(nodoOrigen, nodosVisitados, listaNodos)
    nodosVisitados.append(nodoVoy)
    if ponderado == 1:
        listaAristas.append({
            "source": nodoOrigen,
            "target": nodoDestino,
            "weight": pesoArista,
            "curvature": random.random(), 
                        "rotation": 0
        })
    else:
        listaAristas.append({
            "source": nodoOrigen,
            "target": nodoDestino,
            "curvature": random.random(), 
                        "rotation": 0
        })
    return generarAristasConexasRecursivoNoDirigido(listaNodos, nodosVisitados, nodoVoy+1, listaAristas, ponderado)


def generarNuevoFaltante(origen, nodosVisitado, listaNodos):
    if len(nodosVisitado) == len(listaNodos):
        return origen
    if len(listaNodos) == 1:
        return origen
    temp = choice(listaNodos)
    if temp != origen:
        return temp
    else:
        return generarNuevoFaltante(origen, nodosVisitado, listaNodos)


def generarNuevo(origen, nodosVisitado, listaNodos):
    if len(nodosVisitado) == len(listaNodos):
        return origen
    if len(listaNodos) == 1:
        return origen
    temp = choice(listaNodos)
    if temp["id"] != origen:
        return temp["id"]
    else:
        return generarNuevo(origen, nodosVisitado, listaNodos)


def generarAristasConexasRecursivoDirigido(listaNodos, listaAristas, ponderado):
    faltantes = buscarInaccesibles(listaNodos, listaAristas)
    return generarAristasFaltantes(faltantes, [], listaAristas, len(listaNodos), ponderado)


# me retorna aquellos q no les llega nada
def buscarInaccesiblesNoDirigido(listaNodos: list, listaAristas: list):
    inaccesibles = []
    for i in listaNodos:
        esta = False
        for j in listaAristas:
            if (j["target"] == i["id"] or j["source"] == i["id"]) and j["target"] != j["source"]:
                esta = True
        if not(esta):
            inaccesibles.append(i["id"])
    return inaccesibles


# me retorna aquellos q no les llega nada
def buscarInaccesibles(listaNodos: list, listaAristas: list):
    inaccesibles = []
    for i in listaNodos:
        esta = False
        for j in listaAristas:
            if j["target"] == i["id"] and j["target"] != j["source"]:
                esta = True
        if not(esta):
            inaccesibles.append(i["id"])
    return inaccesibles


def generarAristasFaltantes(listaNodos, nodosVisitados, listaAristas, maximo, ponderado):
    if len(listaNodos) == 1:
        pesoArista = random.randint(5, 20)
        nodoDestino = listaNodos[0]
        nodoOrigen = random.randint(1, maximo)
        if nodoDestino == nodoOrigen and maximo != 1:
            generarAristasFaltantes(
                listaNodos, nodosVisitados, listaAristas, maximo, ponderado)
        if ponderado == 1:
            listaAristas.append({
                "source": nodoOrigen,
                "target": nodoDestino,
                "weight": pesoArista,
                "curvature": random.random(), 
                        "rotation": 0
            })
        else:
            listaAristas.append({
                "source": nodoOrigen,
                "target": nodoDestino,
                "curvature": random.random(), 
                        "rotation": 0
            })
        return listaAristas
    for i in listaNodos:
        pesoArista = random.randint(5, 20)
        nodoOrigen = generarNuevoFaltante(i, nodosVisitados, listaNodos)
        nodoDestino = i
        nodosVisitados.append(i)
        listaAristas.append({
            "source": nodoOrigen,
            "target": nodoDestino,
            "weight": pesoArista,
            "curvature": random.random(), 
                        "rotation": 0
        })
    return listaAristas


def generarMultigrafo(aristas, ponderado):
    pesoArista = random.randint(5, 20)
    nodoOrigen = aristas[0]["source"]
    nodoDestino = aristas[0]["target"]
    if ponderado == 1:
        aristas.append({
            "source": nodoOrigen,
            "target": nodoDestino,
            "weight": pesoArista,
            "curvature": random.random(), 
                        "rotation": 0
        })
    else:
        aristas.append({
            "source": nodoOrigen,
            "target": nodoDestino,
            "curvature": random.random(), 
                        "rotation": 0
        })
    return aristas


def eliminarMultigrafo(aristas: list):
    cont = 0
    for i in aristas:
        contj = 0
        cont = 0
        for j in aristas:
            if i["target"] == j["target"] and i["source"] == j["source"] and contj != contj:
                aristas.pop(cont)
            cont = cont+1
        contj = contj+1
    return aristas


def generarNodosyAristas(conexo):

    if conexo == 1 and not(verificarConexo()):
        generarNodosyAristas(conexo)
    return []


def verificarConexo(nodos, aristas):
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
