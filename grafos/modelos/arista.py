class Arista():
    def __init__(self,origen,destino,peso):
        self.origen=origen
        self.destino=destino
        self.peso=peso
        self.disponible=True
        
    def setdisponible(self,dato):
        self.disponible=dato

    def getorigen(self):
        return self.origen
    def getdisponible(self):
        return self.disponible
    def Cambiodisponible(self):
        if self.disponible:
            self.disponible=False
        else:
            self.disponible = True


    def getdestino(self):
        return self.destino

    def getpeso(self):
        return self.peso
    def setorigen(self,dato):
        self.origen=dato
    def setdestino(self,dato):
        self.destino=dato
    def setpeso(self,dato):
        self.peso=dato