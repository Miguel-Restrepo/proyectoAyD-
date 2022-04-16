from collections import * #esta cosa es de profesor
from Modelo.Vertice import *#importar clase vertice
from Modelo.Arista import *#Importar clase arista
import numpy as np#Libreria Numpy ayuda en el manejo de arreglos
class Grafo():
    def __init__(self):
        self.ListaAristas=[]
        self.ListaVertices=[]
        self.ListaVisitados=[]
        self.ListaVisitadosProfundidad=[]
        self.Pozos=[]
        self.Fuentes=[]
        self.FuerteMenteConexo=False
        self.ListaProhibidos=[]
        self.ListaRecorridoPrim=[]
        self.ListaDisponibles=[]
        self.Contador=0
        self.ListaVerticesVisitados=[]
  

    def ingresarVertice(self,dato):#PUNTO 1 B
        self.ListaVertices.append(Vertice(dato))

    def obtenerVertice(self,dato):#PUNTO 1C-DIRIGIDO
        for Vertice in self.ListaVertices:
            if Vertice.getdato()==dato:
                return Vertice
        return None
    def ingrsarDobleArista(self,origen,destino,peso):#PUNTO 1C- NO DIRIGIDO
        self.ingresarArista(origen,destino,peso)
        self.ingresarArista(destino,origen,peso)
    def ingresarArista(self,origen,destino,peso):
        if self.ObtenerArista(origen,destino)==None:
            if self.obtenerVertice(origen)!=None and self.obtenerVertice(destino)!=None:
                self.ListaAristas.append(Arista(origen,destino,peso))
                self.obtenerVertice(origen).getListaAdyacencia().append(destino)

    def imprimirVertice(self):
        for Vertice in self.ListaVertices:
            print(Vertice.getdato())
            print(Vertice.getListaAdyacencia())
    def imprimirArista(self):
        for Arista in self.ListaAristas:
            print("Origen: {0} - Destino: {1}- Peso: {2}".format(Arista.getorigen(),Arista.getdestino(),Arista.getpeso()))
    def ObtenerArista(self,origen, destino):
        for Arista in self.ListaAristas:
            if Arista.getorigen()==origen and Arista.getdestino()==destino:
                return Arista
        return None
    def RecorridoProfundida(self,dato):#APRENDER PARA PARCIAL
        if dato in self.ListaVisitados:
            return#DEVUELVE A LAVENTANA ANTERIOR
        else:
            Vertice=self.obtenerVertice(dato)
            if Vertice!=None:
                self.ListaVisitados.append(Vertice.getdato())
                for Adyacencias in Vertice.getListaAdyacencia():
                    self.RecorridoProfundida(Adyacencias)

    def getvisitados(self):
        return self.ListaVisitados
    def RecorridoAmplitud(self,dato):#dato es elorigen
        VisitadosA=[]
        cola=deque()
        Vertice=self.obtenerVertice(dato)
        if Vertice!=None:
            cola.append(Vertice)
            VisitadosA.append(dato)

        while cola:
            elemento = cola.popleft()
            for Adyacencias in elemento.getListaAdyacencia():
                if Adyacencias not in VisitadosA:
                    Vertice=self.obtenerVertice(Adyacencias)
                    cola.append(Vertice)
                    VisitadosA.append(Adyacencias)
        return VisitadosA
    def DetectorPozos(self):#PUNTO 1E
        self.Pozos=[]
        #print("El grafo tiene {} Pozo".format(len(self.Pozos)))
        ContadorPozos=0
        for Vertice in self.ListaVertices:
            if len(Vertice.getListaAdyacencia())==0:
                ContadorPozos=ContadorPozos+1
                self.Pozos.append(Vertice.getdato())
       # print("El grafo tiene {} Pozo".format(len(self.Pozos)))
    def CuantasFuentes(self):#Punto 1 F
        return len(self.Fuentes)
    def CuantosPozos(self):#Punto 1 F
        return len(self.Pozos)
    def DetectorFuente(self,dato):
        for Vertice in self.ListaVertices:
            for adyacencia in Vertice.getListaAdyacencia():
                if adyacencia==dato:
                    return False #Si se encuentra en una adyacencia, ya no puede ser fuente
        self.Fuentes.append(dato)
        return True
    def DetectorFuentes(self):
        self.Fuentes=[]
        for VerticeP in self.ListaVertices:
            self.DetectorFuente(VerticeP.getdato())
        #print("El grafo tiene {} Fuentes".format(len(self.Fuentes)))
    def VerificarSiEsFuertementeConexo(self):#PUNTO 1 D
        self.DetectorFuentes()
        self.DetectorPozos()
        if len(self.Fuentes)==0 and len(self.Pozos)==0:
           self.FuerteMenteConexo=True
        else:
           self.FuerteMenteConexo=False
    def ImprimirAristaDescendente(self):
        ListaOrdenada = []
        for dato in self.ListaAristas:#For para llenar la lista
            ListaOrdenada.append(dato.getpeso())
        for numPasada in range(len(ListaOrdenada) - 1, 0, -1):
            for i in range(numPasada):
                if ListaOrdenada[i] < ListaOrdenada[i + 1]:
                    temp = ListaOrdenada[i]
                    ListaOrdenada[i] = ListaOrdenada[i + 1]
                    ListaOrdenada[i + 1] = temp
        print(ListaOrdenada)

    def ImprimirAristaDescendenteOrigen_Ciudad(self):
        ListaOrdenada = self.ListaAristas
        print("Las Aristas de forma descendente son")
        for numPasada in range(len(ListaOrdenada) - 1, 0, -1):
            for i in range(numPasada):
                if ListaOrdenada[i].getpeso() < ListaOrdenada[i + 1].getpeso():
                    temp = ListaOrdenada[i]
                    ListaOrdenada[i] = ListaOrdenada[i + 1]
                    ListaOrdenada[i + 1] = temp
        for dato in ListaOrdenada:#For para llenar la lista
            print("Origen: {} Destino: {} Destancia: {}".format(dato.getorigen(),dato.getdestino(),dato.getpeso()))

    def RecorridoProfundidaMio(self, dato):  # APRENDER PARA PARCIAL
        if dato in self.ListaVisitadosProfundidad:
            return  # DEVUELVE A LAVENTANA ANTERIOR
        else:
            Vertice = self.obtenerVertice(dato)
            if Vertice != None:
                self.ListaVisitadosProfundidad.append(Vertice.getdato())
                for Adyacencias in Vertice.getListaAdyacencia():
                    self.RecorridoProfundidaMio(Adyacencias)

    def CambiarSentido(self,arista):#PUNTO 2B
        origen=arista.getdestino()
        destino=arista.getorigen()
        peso=arista.getpeso()
        self.ListaAristas.remove(arista)
        self.ListaAristas.append(Arista(origen,destino,peso))



    def SolicitarPedido(self, hachas, palas, agua, picas,martillos, destino,centro):
        destino=self.obtenerVertice(destino)
        camion=None
        for camionbuscador in centro.Camiones:
            if len(camionbuscador.ListaPedidos)<5:
                camion=camionbuscador
                break
            else:
                print("buscando Siguiente Camion")
        if camion==None:
            print("No hay actualmente Camiones Disponibles")
            return
        if hachas>centro.getHachasAlmacenadas() or palas>centro.getPalasAlmacenadas() or agua>centro.getAguaAlmacenada() or picas>centro.getPicasAlmacenadas() or martillos>centro.getMartillosAlmacenados():
            print("No es posible Realizar el pedido")
            return
        else:
            centro.DisminuirHachas(hachas)
            centro.DisminuirPalas(palas)
            centro.DisminuirAgua(agua)
            centro.DisminuirPicas(picas)
            centro.DisminuirMartillos(martillos)
            PedidoNuevo=Pedido(destino,hachas,palas,agua,picas,martillos, camion)
            camion.ListaPedidos.append(PedidoNuevo)
            print("Solicitado")
    def DesbloquearArista(self,origen,destino):
        arista = self.ObtenerArista(origen, destino)
        aristavuelta = self.ObtenerArista(destino, origen)
        if arista != None:
            arista.setdisponible(True)
        if aristavuelta != None:
            aristavuelta.setdisponible(True)
    def BloquearArista(self,origen,destino):#punto 2 A
        arista=self.ObtenerArista(origen,destino)
        aristavuelta = self.ObtenerArista(destino, origen)
        if arista!=None:
            arista.setdisponible(False)
        if aristavuelta != None:
            aristavuelta.setdisponible(False)

    def RecorridoPuntoPunto(self, origen, destino):#PUNTO 2C
        NodoVoy = origen
        origen=self.obtenerVertice(origen)
        #destino=self.obtenerVertice(destino)
        ListaRecorrer=[]
        NoIr=[]

        while (True):
            for arista in self.ListaAristas:
                aristaHipotetica = self.ObtenerArista(NodoVoy, destino)
                if aristaHipotetica != None:  # if para cortar caminos
                    if aristaHipotetica.getdisponible():
                        ListaRecorrer.append(aristaHipotetica)
                        return ListaRecorrer

                if arista.getdisponible() and arista.getorigen()==NodoVoy and not(arista.getdestino() in NoIr):

                    ListaRecorrer.append(arista)
                    NoIr.append(arista.getdestino())
                    NoIr.append(arista.getorigen())
                    if arista.getdestino()==destino:
                        return ListaRecorrer
                    if len(ListaRecorrer)>len(self.ListaVertices)-4:
                        print("IMPOSIBLE LLEGAR")
                        return False
                    NodoVoy=arista.getdestino()
                    break

    def EncontrarDisponible(self,vertice):#Obtiene todas las aristas y agrega a lista de disponibles
        for Arista in self.ListaAristas:
            if Arista.getorigen()==vertice:
                f=len(self.ListaRecorridoPrim)
                if f>0:
                    destinoPro=self.ListaRecorridoPrim[f-1].getorigen()
                else:
                    destinoPro=""
                #print(destinoPro)
                if Arista.getdestino()!=destinoPro:
                    self.ListaDisponibles.append(Arista)
        self.EliminarProhibidosDisponible()
        self.OrdenarBurbujaAristas()

    def EliminarProhibidosDisponible(self):#Elimina elementos prohibidos de disponible
        ListaD=self.ListaDisponibles
        ListaP=self.ListaProhibidos
        for i in ListaP:
            AristaTemporal=i
            if AristaTemporal in ListaD:
                ListaD.remove(i)
        self.ListaDisponibles=ListaD
    def OrdenarBurbujaAristas(self):#Ordena por burbuja segun el peso las aristas de menor a mayor
        self.EliminarRepetidos()
        ListaOrdenada = self.ListaDisponibles
        for numPasada in range(len(ListaOrdenada) - 1, 0, -1):
            for i in range(numPasada):
                if ListaOrdenada[i].getpeso() > ListaOrdenada[i + 1].getpeso():
                    temp = ListaOrdenada[i]
                    ListaOrdenada[i] = ListaOrdenada[i + 1]
                    ListaOrdenada[i + 1] = temp
        self.ListaDisponibles=ListaOrdenada



    def EliminarRepetidos(self):
        ListaRepetidos=self.ListaDisponibles
        ListaSinRepetidos = []
        for i in ListaRepetidos:
            if i not in ListaSinRepetidos:
                ListaSinRepetidos.append(i)
        self.ListaDisponibles=ListaSinRepetidos


    def EvitaCiclos(self):#Evitatodo posible cierre de ciclos
        ListaVertices=self.ListaVerticesVisitados
        for origen in ListaVertices:
            for destino in ListaVertices:
                Aristatmp=self.ObtenerArista(origen,destino)
                self.ListaProhibidos.append(Aristatmp)

    def RecorridoPrim(self,vertice):
        if self.Contador==0:
            self.BidireccionarGrafo()
            self.ListaVerticesVisitados.append(vertice)
        if vertice== None or self.Contador>(len(self.ListaVertices)-2) :
            print("Finalizo")
            return
        self.Contador=self.Contador+1
        self.EliminarProhibidosDisponible()
        self.EncontrarDisponible(vertice)#Arrroja aristas posibles
        self.ListaRecorridoPrim.append(self.ListaDisponibles[0])
        destino = self.ListaDisponibles[0].getdestino()
        self.ListaProhibidos.append(self.ListaDisponibles[0])
        AristaInversa=Arista(self.ListaDisponibles[0].getdestino(),self.ListaDisponibles[0].getorigen(),self.ListaDisponibles[0].getpeso())
        self.ListaProhibidos.append(AristaInversa)
        self.EliminarProhibidosDisponible()
        self.ListaVerticesVisitados.append(destino)
        self.EvitaCiclos()
        self.RecorridoPrim(destino)



    def EliminarRepetidosRedireccion(self):
        ListaRepetidos=self.ListaAristas
        ListaSinRepetidos = []
        for i in ListaRepetidos:
            if i not in ListaSinRepetidos:
                ListaSinRepetidos.append(i)
        self.ListaAristas=ListaSinRepetidos

    def BidireccionarGrafo(self):#Convierte en no dirigido
        for arista in self.ListaAristas:
            self.ingresarArista(arista.getdestino(),arista.getorigen(),arista.getpeso())
        self.EliminarRepetidosRedireccion()


    def Boruvka(self):
        copiaNodos = []
        for aristaNueva in self.ListaVertices:
            copiaNodos.append(aristaNueva)
        copiaAristas = []
        for aristaNueva in self.ListaAristas:
            copiaAristas.append(aristaNueva)
        #copiaNodos = copy(self.Listavertices)  # copia de los nodos
        #copiaAristas = copy(self.ListaAristas)  # copia de las aristas

        AristasBorukvka = []
        ListaConjuntos = []
        bandera = True
        cantidad = 0
        while (cantidad > 1 or bandera):
            for Nodo in copiaNodos:
                self.OperacionesconjuntosB(Nodo, ListaConjuntos, AristasBorukvka, copiaAristas)
            bandera = False;
            cantidad = self.Cantidadconjuntos(ListaConjuntos)

        for dato in AristasBorukvka:
            print("Origen: {0} destino: {1} peso: {2}".format(dato.getorigen(), dato.getdestino(), dato.getpeso()))
        return AristasBorukvka

    def Cantidadconjuntos(self, ListaConjuntos):
        cantidad = 0
        for conjunto in ListaConjuntos:
            if len(conjunto) > 0:
                catidad = cantidad + 1
        return cantidad

    def OperacionesconjuntosB(self, Nodo, ListaConjuntos, AristasBorukvka, copiaAristas):
        encontrado1 = -1
        encontrado2 = -1
        menor = self.Buscarmenor(Nodo, copiaAristas)

        if not menor == None:  # si no esta vacio
            if not ListaConjuntos:  # si esta vacia
                ListaConjuntos.append({menor.getorigen(), menor.getdestino()})
                AristasBorukvka.append(menor)
            else:
                for i in range(len(ListaConjuntos)):
                    if (menor.getorigen() in ListaConjuntos[i]) and (menor.getdestino() in ListaConjuntos[i]):
                        return False;  ##Camino cicliclo

                for i in range(len(ListaConjuntos)):
                    if menor.getorigen() in ListaConjuntos[i]:
                        encontrado1 = i
                    if menor.getdestino() in ListaConjuntos[i]:
                        encontrado2 = i

                if encontrado1 != -1 and encontrado2 != -1:
                    if encontrado1 != encontrado2:  # si pertenecen a dos conjuntos diferentes
                        # debo unir los dos conjuntos
                        ListaConjuntos[encontrado1].update(ListaConjuntos[encontrado2])
                        ListaConjuntos[encontrado2].clear();  # elimino el conjunto
                        AristasBorukvka.append(menor)

                if encontrado1 != -1 and encontrado2 == -1:  # si va unido por un conjunto
                    ListaConjuntos[encontrado1].update(menor.getorigen())
                    ListaConjuntos[encontrado1].update(menor.getdestino())
                    AristasBorukvka.append(menor)

                if encontrado1 == -1 and encontrado2 != -1:  # si va unido por un conjunto
                    ListaConjuntos[encontrado2].update(menor.getorigen())
                    ListaConjuntos[encontrado2].update(menor.getdestino())
                    AristasBorukvka.append(menor)

                if encontrado1 == -1 and encontrado2 == -1:  # si no existe en los conjuntos
                    ListaConjuntos.append({menor.getorigen(), menor.getdestino()})
                    AristasBorukvka.append(menor)

    def Buscarmenor(self, Nodo, copiaAristas):
        temp = []
        for adyacencia in Nodo.getListaAdyacencia():
            for Arista in copiaAristas:
                # busco las aristas de esa lista de adyacencia
                if Arista.getorigen() == Nodo.getdato() and Arista.getdestino() == adyacencia:
                    temp.append(Arista)
        if temp:  # si no esta vacia
            # una vez obtenga todas las aristas, saco la menor
            self.ordenamiento(temp)  # ordeno las aristas
            # elimin ese destino porque ya lo voy a visitar
            # print("{0}-{1}:{2}".format(temp[0].getOrigen(), temp[0].getDestino(), temp[0].getPeso()))

            Nodo.getListaAdyacencia().remove(temp[0].getdestino())
            return temp[0]  # es la menor

        return None  # es la menor





    def Kruskal(self):
        copiaAristas=[]
        for aristaNueva in self.ListaAristas:
            copiaAristas.append(aristaNueva)
#        copiaAristas = copy(self.ListaAristas)  # copia de las aristas
        AristasKruskal = []
        ListaConjuntos = []

        self.ordenamiento(copiaAristas)  # ordeno las aristas
        for menor in copiaAristas:
            self.Operacionesconjuntos(menor, ListaConjuntos, AristasKruskal)
        # esta ordenada de mayor a menor
        print("-----------Kruskal---------------")
        for dato in AristasKruskal:
            print("Origen: {0} destino: {1} peso: {2}".format(dato.getorigen(), dato.getdestino(), dato.getpeso()))
        return AristasKruskal
    def ordenamiento(self,lista):#Ordena por burbuja segun el peso las aristas de menor a mayor
        for numPasada in range(len(lista) - 1, 0, -1):
            for i in range(numPasada):
                if lista[i].getpeso() > lista[i + 1].getpeso():
                    temp = lista[i]
                    lista[i] = lista[i + 1]
                    lista[i + 1] = temp
        return lista

    def Operacionesconjuntos(self, menor, ListaConjuntos, AristasKruskal):
        encontrado1 = -1
        encontrado2 = -1

        if not ListaConjuntos:  # si esta vacia
            ListaConjuntos.append({menor.getorigen(), menor.getdestino()})
            AristasKruskal.append(menor)

        else:
            for i in range(len(ListaConjuntos)):
                if (menor.getorigen() in ListaConjuntos[i]) and (menor.getdestino() in ListaConjuntos[i]):
                    return  ##Camino cicliclo

            for i in range(len(ListaConjuntos)):
                if menor.getorigen() in ListaConjuntos[i]:
                    encontrado1 = i
                if menor.getdestino() in ListaConjuntos[i]:
                    encontrado2 = i

            if encontrado1 != -1 and encontrado2 != -1:
                if encontrado1 != encontrado2:  # si pertenecen a dos conjuntos diferentes
                    # debo unir los dos conjuntos
                    ListaConjuntos[encontrado1].update(ListaConjuntos[encontrado2])
                    # este update si funciona correctemente
                    ListaConjuntos[encontrado2].clear()  # elimino el conjunto
                    AristasKruskal.append(menor)

            if encontrado1 != -1 and encontrado2 == -1:  # si va unido por un conjunto
                # el update se cambio con por el add ya que al agregar cadenas a Listaconjuntos
                # no se guardaba como "Silvestre" sino que la desglosaba en sus caracteres "S,i,l,v,e,t,r,e" en Listaconjuntos
                ListaConjuntos[encontrado1].add(menor.getorigen())
                ListaConjuntos[encontrado1].add(menor.getdestino())
                AristasKruskal.append(menor)

            if encontrado1 == -1 and encontrado2 != -1:  # si va unido por un conjunto
                ListaConjuntos[encontrado2].add(menor.getorigen())
                ListaConjuntos[encontrado2].add(menor.getdestino())
                AristasKruskal.append(menor)

            if encontrado1 == -1 and encontrado2 == -1:  # si no existe en los conjuntos
                ListaConjuntos.append({menor.getorigen(), menor.getdestino()})
                AristasKruskal.append(menor)


  
    def caminoMasCorto(self, origen, destino):
        VerticesAux = []
        VerticesD = []
        caminos = self.dijkstra(origen, VerticesAux)
        cont = 0
        for i in caminos:
            print("La distancia mínima a: " + self.ListaVertices[cont].getDato() + " es " + str(i))
            cont = cont + 1

        self.rutas(VerticesD, VerticesAux, destino, origen)
        print("El camino más corto de: " + origen + " a " + destino + " es: ")
        print(VerticesD)

    def rutas(self, VerticesD, VerticesAux, destino, origen):
        verticeDestino = self.obtenervertice(destino)
        indice = self.ListaVertices.index(verticeDestino)
        if VerticesAux[indice] is None:
            print("No hay camino entre: ", (origen, destino))
            return
        aux = destino
        while aux is not origen:
            verticeDestino = self.obtenervertice(aux)
            indice = self.ListaVertices.index(verticeDestino)
            VerticesD.insert(0, aux)
            aux = VerticesAux[indice]
        VerticesD.insert(0, aux)

    def dijkstra(self, origen, VerticesAux):
        marcados = []  # la lista de los que ya hemos visitado
        caminos = []  # la lista final
        # iniciar los valores en infinito
        for v in self.ListaVertices:
            caminos.append(float("inf"))
            marcados.append(False)
            VerticesAux.append(None)
            if v.getdato() is origen:
                caminos[self.ListaVertices.index(v)] = 0
                VerticesAux[self.ListaVertices.index(v)] = v.getDato()
        while not self.todosMarcados(marcados):
            aux = self.menorNoMarcado(caminos, marcados)  # obtuve el menor no marcado
            if aux is None:
                break
            indice = self.ListaVertices.index(aux)  # indice del menor no marcado
            marcados[indice] = True  # marco como visitado
            valorActual = caminos[indice]
            for vAdya in aux.getListaAdyacentes():
                indiceNuevo = self.ListaVertices.index(self.obtenervertice(vAdya))
                arista = self.verificararista(vAdya, aux.getDato())
                if caminos[indiceNuevo] > valorActual + arista.getPeso():
                    caminos[indiceNuevo] = valorActual + arista.getPeso()
                    VerticesAux[indiceNuevo] = self.ListaVertices[indice].getDato()
        return caminos

    def menorNoMarcado(self, caminos, marcados):
        verticeMenor = None
        caminosAux = sorted(caminos)
        copiacaminos=[]
        for f in caminos:
            copiacaminos.append(f)
        bandera = True
        contador = 0
        while bandera:
            menor = caminosAux[contador]
            if marcados[copiacaminos.index(menor)] == False:
                verticeMenor = self.ListaVertices[copiacaminos.index(menor)]
                bandera = False
            else:
                copiacaminos[copiacaminos.index(menor)] = "x"
                contador = contador + 1
        return verticeMenor

    def todosMarcados(self, marcados):
        for j in marcados:
            if j is False:
                return False
        return True

    def EliminarNodo(self,nodo):
        Nodo=self.obtenerVertice(nodo)
        for x in self.ListaVertices:
            conectada=self.ObtenerArista(x.getdato(),nodo)
            if conectada!=None:
                self.ListaAristas.remove(conectada)
            conectada = self.ObtenerArista(nodo, x.getdato())
            if conectada != None:
                self.ListaAristas.remove(conectada)
        self.ListaVertices.remove(Nodo)

    def EliminarArista(self, origen, destino):
        AristaIda = self.ObtenerArista(origen, destino)
        AristaVuelta = self.ObtenerArista(destino, origen)
        self.ListaAristas.remove(AristaIda)
        self.ListaAristas.remove(AristaVuelta)