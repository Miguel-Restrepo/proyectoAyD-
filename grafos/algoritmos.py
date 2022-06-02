import logging
from grafos.algoritmos_code.Queyranne import *
from grafos.algoritmos_code.Q_Clustering import *


def AlgoritQueyranne(grafo):
    logging.info(grafo)
    return QUEYRANNE(grafo.nodes, grafo )

def AlgoritmoMssf(grafo):
    return grafo    
def AlgoritQ_Clustering(grafo):
    return Q_Clustering(grafo)
