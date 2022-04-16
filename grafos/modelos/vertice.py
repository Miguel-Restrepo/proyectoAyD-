class Vertice():
    def __init__(self,dato):
        self.dato=dato
        self.ListaAdyacencia=[]
    def getdato(self):
        return self.dato
    def getListaAdyacencia(self):
        return self.ListaAdyacencia
    def setdato(self,dato):
        self.dato=dato
    def setListaAdyacencia(self,dato):
        self.ListaAdyacencia=dato