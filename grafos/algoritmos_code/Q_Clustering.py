import math
import sys
from random import shuffle, uniform

def leerInformacion(grafo):
    items = []
    for i in range(1,len(grafo.links)):
        line = grafo.links[i]
        itemFeatures = []
        v = float(line.weight)
        itemFeatures.append(v) 
        items.append(itemFeatures)
    shuffle(items)
    return items

def FindColMinMax(items):
    n = len(items[0])
    minima = [sys.maxsize for i in range(n)]
    maxima = [-sys.maxsize -1 for i in range(n)]
    for item in items:
        for f in range(len(item)):
            if(item[f] < minima[f]):
                minima[f] = item[f]
            
            if(item[f] > maxima[f]):
                maxima[f] = item[f]

    return minima,maxima
#uma al cuadrado de la diferencia
def EuclideanDistance(x,y):
    S = 0 
    for i in range(len(x)):
        S += math.pow(x[i]-y[i],2)

    return math.sqrt(S) 

    #inicializa media ramdon numero
    #minimo y maximo por columna
def InitializeMeans(items,k,cMin,cMax):
    f = len(items[0]) #number of features
    means = [[0 for i in range(f)] for j in range(k)]
    for mean in means:
        for i in range(len(mean)):
            mean[i] = uniform(cMin[i]+1,cMax[i]-1)
    return means

def UpdateMean(n,mean,item):
    for i in range(len(mean)):
        m = mean[i]
        m = (m*(n-1)+item[i])/float(n)
        mean[i] = round(m,3)
    return mean

def FindClusters(means,items):
    clusters = [[] for i in range(len(means))] 
    for item in items:
        index = Classify(means,item)
        clusters[index].append(item)
    return clusters

#clasificamos por peso
def Classify(means,item):
    minimum = sys.maxsize
    index = -1
    for i in range(len(means)):
        #calcula distancia
        dis = EuclideanDistance(item,means[i])
        if(dis < minimum):
            minimum = dis
            index = i
    
    return index

def calcularMeans(k,items,maxIterations=200):
    cMin, cMax = FindColMinMax(items)
    means = InitializeMeans(items,k,cMin,cMax)
    clusterSizes = [0 for i in range(len(means))]
    belongsTo = [0 for i in range(len(items))]
    for e in range(maxIterations):
        noChange = True
        for i in range(len(items)):
            item = items[i]
            index = Classify(means,item)
            clusterSizes[index] += 1
            means[index] = UpdateMean(clusterSizes[index],means[index],item)
            if(index != belongsTo[i]):
                noChange = False

            belongsTo[i] = index


        if(noChange):
            break

    return means

def calcularValoresPerdidos(clusters, means):

    m = len(clusters)
    totalLoss = 0
    for i in range(len(clusters)):
        for item in clusters[i]:
            loss = EuclideanDistance(item, means[i])
            totalLoss += math.pow(loss, 2)

    return totalLoss / m


def Q_Clustering(grafo):
    items = leerInformacion(grafo)
    valoresPerdidos = []

    for k in range(1, 40):
        means = calcularMeans(k,items)
        clusters = FindClusters(means,items)
        lossValue = calcularValoresPerdidos(clusters, means)
        valoresPerdidos.append(lossValue)
        print(math.sqrt(lossValue))
    grafo.nodes=means
    grafo.links=clusters
    return grafo
