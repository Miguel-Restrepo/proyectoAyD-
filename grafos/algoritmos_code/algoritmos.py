import math  # For pow and sqrt
from random import shuffle, uniform
import sys
import random
import time
# --------------------------------------------------QUEYRANNE 2 PARTICIONES-------------------------------------------
#from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import numpy.linalg as la
import copy
#from collections import Sequence
from itertools import chain, count
from scipy.linalg import block_diag
from typing import Any

# -*- Some useful preliminary functions -*-


def trinv(matrix):
    tri = np.trace(la.inv(matrix))
    return tri


def permutation_matrix(n):
    rr = range(n)
    np.random.shuffle(rr)
    P = np.take(np.eye(n), rr, axis=0)
    return P


def select_mat(matrix, index_row, index_column):
    # sort the row/cols lists
    index_row.sort()
    index_column.sort()
    index_row = list(set(index_row))
    index_column = list(set(index_column))
    S = np.transpose(np.transpose(matrix[index_row])[index_column])
    return S


def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]


def ismember(a, B):
    response = False
    index = 0
    while response == False and index < len(B):
        b = B[index]
        if b == a:
            return True
        else:
            index = index+1

    return response


def partition(collection):
    if len(collection) == 1:
        yield [collection]
        return
    first = collection[0]
    for smaller in partition(collection[1:]):
        # insert `first` in each of the subpartition's subsets
        for n, subset in enumerate(smaller):
            yield smaller[:n] + [[first] + subset] + smaller[n+1:]
        # put `first` in its own subset
        yield [[first]] + smaller


def select_from_list(list, indices):
    list_select = [list[i] for i in indices]
    return list_select


# Finding a pendent-pair of a supermodular system(V,f):
# For a given sets W and Q, find the most far element
# in Q to W
# W and Q should be list of lists to account for fused elements

def Find_Far_Element(SS, F, WW, QQ):

    # Find the most far element to WW in QQ

    u = QQ[0]  # a list not an index
    W_cp = copy.copy(WW)
    W_cp.append(u)
    dist_max = F(SS, W_cp) - F(SS, u)
    elt_far = u
    Q_ = copy.copy(QQ)
    Q_.remove(u)
    for elt in Q_:
        W_cp = copy.copy(WW)
        W_cp.append(elt)
        dist_elt = F(SS, W_cp) - F(SS, elt)
        if dist_elt > dist_max:
            dist_max = dist_elt
            elt_far = elt

    return elt_far

# ----- Finding a pendent pair is a fundamental step in Queyranne's algorithm ----- #


def PENDENT_PAIR(SS, VV, F):

    # V is the set of all points including fused pairs
    # The size of V goes from n to 2
    # Start with a random element in V

    V_ = copy.copy(VV)
    rnd_pattern = np.random.permutation(len(V_))
    #x = V_[rnd_pattern[0]]
    x = V_[0]
    if type(x) == list:
        W = x
    else:
        W = [x]
    Q = copy.copy(V_)
    Q.remove(x)
    V_.remove(x)
    for i in range(len(V_)):
        elt_far = Find_Far_Element(SS, F, W, Q)
        W.append(elt_far)
        Q.remove(elt_far)

    return W[-2], W[-1]


def tr_inv(SS, set):
    """
    :rtype: float
    """
    if type(set) == int:
        LIST = [set]
    else:
        LIST = []
        for i in range(len(set)):
            if type(set[i]) == list:
                LIST.extend(set[i])
            else:
                LIST.append(set[i])

    return trinv(select_mat(SS, LIST, LIST))


def log_det(SS, set):
    """
    :rtype: float
    """
    if type(set) == int:
        LIST = [set]
    else:
        LIST = []
        for i in range(len(set)):
            if type(set[i]) == list:
                LIST.extend(set[i])
            else:
                LIST.append(set[i])

    return -np.log(la.det(select_mat(SS, LIST, LIST)))


def fuse(A, B):
    if type(A) == int and type(B) == int:
        f = [A, B]
    elif type(A) == int and type(B) == list:
        f = [A] + B
    elif type(A) == list and type(B) == int:
        f = A + [B]
    elif type(A) == list and type(B) == list:
        f = A + B

    return f

# -*- Full implementation of Queyranne's algorithm -*-
def QueyranneIniciar(grafo):
    items = convertir(grafo)
    items= np.array(items)
    print(items)
    # Empezamos a contar el tiempo
    inicial = time.time()
    F=None
    subset_opt, partition_value, cluster_max =QUEYRANNE(items,F)
    final = time.time()
    grafo["tiempo"] = final-inicial
    return desconvertir(grafo, subset_opt)

def QUEYRANNE(SS, F):
    # """" type: (matrix, function) -> (list, float, list)

    dim, _ = SS.shape
    # is the space of points which is updated at each step we find a pendent pair
    V = range(dim)
    C = []  # set of candidates updated at each step
    while len(V) >= 3:
        W = copy.deepcopy(V)
        a, b = PENDENT_PAIR(SS, W, F)  # find a pendent pair in (V,F)
        if type(b) == int:
            C.append([b])
        else:
            C.append(b)

        fus = fuse(a, b)  # fuse this pair as a list
        V.append(fus)
        if ismember(a, V) is True and ismember(b, V) is True:
            V.remove(a)
            V.remove(b)

    for subset in V:
        if type(subset) == int:
            C.append([subset])
        else:
            C.append(subset)

    #  Once we have the list of candidates, we return the best one
    max_value = -np.Inf
    subset_opt = []
    cluster_max = 0
    partition_value = 0
    for subset in C:
        cluster_value = F(SS, subset)
        subset_value = cluster_value + F(SS, diff(range(dim), subset))
        if subset_value > max_value:
            subset_opt = subset
            partition_value = subset_value
            cluster_max = cluster_value
            max_value = subset_value

    return subset_opt, partition_value, cluster_max






























# -------------------------------------------------Q_CLUSTERING Bi PARTICIONES-------------------------------------------

def desconvertirBi(grafo, particiones):
    colores = ["#1976D2", "#E13918"]
    divisor = round(particiones[0][0])
    if divisor == 1:
        divisor = divisor+1
    color = -1
    for mean in particiones:
        color = color+1
        for nodo in grafo["nodes"]:
            if nodo['id'] >= round(mean[0]):
                nodo["color"] = colores[0]
            else:
                nodo["color"] = colores[1]
    links = []
    
    for arista in grafo["links"]:
        try:
            if not arista["source"]["id"]:
                if arista["target"] >= divisor and arista["source"] >= divisor:
                    links.append(arista)
                elif arista["target"] < divisor and arista["source"] < divisor:
                    links.append(arista)
            elif arista["target"]["id"] >= divisor and arista["source"]["id"] >= divisor:
                if grafo["Ponderado"] == 1:
                    nuevolink = {
                        "source": arista["source"]["id"],
                        "target": arista["target"]["id"],
                        "weight": arista["weight"]
                    }
                else:
                    nuevolink = {
                        "source": arista["source"]["id"],
                        "target": arista["target"]["id"]
                    }
                links.append(nuevolink)
            elif arista["target"]["id"] < divisor and arista["source"]["id"] < divisor:

                if grafo["Ponderado"] == 1:
                    nuevolink = {
                        "source": arista["source"]["id"],
                        "target": arista["target"]["id"],
                        "weight": arista["weight"]
                    }
                else:
                    nuevolink = {
                        "source": arista["source"]["id"],
                        "target": arista["target"]["id"]
                    }

                links.append(nuevolink)
        except:
            if arista["target"] >= divisor and arista["source"] >= divisor:
                links.append(arista)
            elif arista["target"] < divisor and arista["source"] < divisor:
                links.append(arista)

    grafo["links"] = links
    return grafo
# PRINCIPAL


def ejecutarQclusteringBi(grafo):
    items = convertir(grafo)
    # Empezamos a contar el tiempo
    inicial = time.time()
    lossValues = []
    means = []  # PAra evitar errores
    for k in range(1, 3):
        means = CalculateMeans(k, items)
        clusters = FindClusters(means, items)
        lossValue = CalculateLossValue(clusters, means)
        lossValues.append(lossValue)
        print(math.sqrt(lossValue))
    # dejamos de contar el tiempo
    final = time.time()
    grafo["tiempo"] = final-inicial
    return desconvertirBi(grafo, means)

























# -------------------------------------------------Q_CLUSTERING K PARTICIONES-------------------------------------------
# import threading #Hilo para grafica
# Convierte lo original en el formato necesitado


def convertir(grafo):
    items = []
    for nodo in grafo["nodes"]:
        for arista in grafo["links"]:
            try:
                if not arista["source"]["id"]:
                    if nodo["id"] == arista["source"]:
                        items.append([nodo["id"], nodo["val"]*arista["weight"],
                                     nodo["val"], arista["weight"], arista["target"], nodo["id"]])
                elif nodo["id"] == arista["source"]["id"]:
                    if grafo["Ponderado"] == 1:
                        items.append([nodo["id"], nodo["val"]*arista["weight"], nodo["val"],
                                     arista["weight"], arista["target"]["id"], nodo["id"]])
                    else:  # SI NO ES Ponderado NO SE HARIA NADA, POR ENDE SE LE DA VALORES PARA CALCULAR TERMPORASLEMTE
                        items.append([nodo["id"], random.randint(5, 20), random.randint(
                            5, 20), random.randint(5, 20), arista["target"]["id"], nodo["id"]])
            except:
                if nodo["id"] == arista["source"]:
                    items.append([nodo["id"], nodo["val"]*arista["weight"],
                                 nodo["val"], arista["weight"], arista["target"], nodo["id"]])

    return items
    # return  [[25.0, 98.0, 80.0, 2126.0, 17.0], [23.0, 97.0, 54.0, 2254.0, 24.0], [29.0, 135.0, 84.0, 2525.0, 16.0], [27.2, 119.0, 97.0, 2300.0, 15.0], [31.5, 98.0, 68.0, 2045.0, 19.0], [26.0, 96.0, 69.0, 2189.0, 18.0], [36.4, 121.0, 67.0, 2950.0, 20.0], [20.6, 225.0, 110.0, 3360.0, 17.0], [24.0, 200.0, 81.0, 3012.0, 18.0], [23.0, 140.0, 83.0, 2639.0, 17.0], [22.4, 231.0, 110.0, 3415.0, 16.0], [18.0, 70.0, 90.0, 2124.0, 14.0], [26.0, 79.0, 67.0, 1963.0, 16.0], [30.9, 105.0, 75.0, 2230.0, 15.0], [40.8, 85.0, 65.0, 2110.0, 19.0], [18.1, 302.0, 139.0, 3205.0, 11.0], [19.0, 232.0, 100.0, 2634.0, 13.0], [24.3, 151.0, 90.0, 3003.0, 20.0], [21.6, 121.0, 115.0, 2795.0, 16.0], [31.0, 76.0, 52.0, 1649.0, 17.0], [18.0, 307.0, 130.0, 3504.0, 12.0], [15.0, 250.0, 72.0, 3158.0, 20.0], [17.0, 302.0, 140.0, 3449.0, 11.0], [17.6, 225.0, 85.0, 3465.0, 17.0], [26.0, 98.0, 90.0, 2265.0, 16.0], [31.8, 85.0, 65.0, 2020.0, 19.0], [32.7, 168.0, 132.0, 2910.0, 11.0], [26.0, 97.0, 46.0, 1950.0, 21.0], [16.0, 400.0, 180.0, 4220.0, 11.0], [29.5, 97.0, 71.0, 1825.0, 12.0], [17.5, 318.0, 140.0, 4080.0, 14.0], [12.0, 429.0, 198.0, 4952.0, 12.0], [20.8, 200.0, 85.0, 3070.0, 17.0], [22.0, 146.0, 97.0, 2815.0, 15.0], [14.0, 351.0, 148.0, 4657.0, 14.0], [20.0, 198.0, 95.0, 3102.0, 17.0], [22.0, 108.0, 94.0, 2379.0, 17.0], [23.0, 198.0, 95.0, 2904.0, 16.0], [34.2, 105.0, 70.0, 2200.0, 13.0], [15.0, 400.0, 150.0, 3761.0, 10.0], [14.0, 318.0, 150.0, 4096.0, 13.0], [18.0, 318.0, 150.0, 3436.0, 11.0], [14.0, 318.0, 150.0, 4457.0, 14.0], [16.0, 351.0, 149.0, 4335.0, 15.0], [15.5, 351.0, 142.0, 4054.0, 14.0], [20.3, 131.0, 103.0, 2830.0, 16.0], [25.0, 110.0, 87.0, 2672.0, 18.0], [17.5, 305.0, 140.0, 4215.0, 13.0], [23.9, 260.0, 90.0, 3420.0, 22.0], [22.0, 225.0, 100.0, 3233.0, 15.0], [26.5, 140.0, 72.0, 2565.0, 14.0], [13.0, 350.0, 145.0, 3988.0, 13.0], [36.1, 91.0, 60.0, 1800.0, 16.0], [23.0, 140.0, 78.0, 2592.0, 19.0], [17.7, 231.0, 165.0, 3445.0, 13.0], [31.0, 112.0, 85.0, 2575.0, 16.0], [14.0, 350.0, 165.0, 4209.0, 12.0], [43.1, 90.0, 48.0, 1985.0, 22.0], [13.0, 318.0, 150.0, 3940.0, 13.0], [21.0, 140.0, 72.0, 2401.0, 20.0], [16.0, 304.0, 150.0, 3433.0, 12.0], [29.9, 98.0, 65.0, 2380.0, 21.0], [13.0, 400.0, 150.0, 4464.0, 12.0], [29.0, 97.0, 75.0, 2171.0, 16.0], [31.9, 89.0, 71.0, 1925.0, 14.0], [28.0, 90.0, 75.0, 2125.0, 15.0], [18.0, 121.0, 112.0, 2933.0, 15.0], [15.0, 383.0, 170.0, 3563.0, 10.0], [29.0, 98.0, 83.0, 2219.0, 17.0], [22.5, 232.0, 90.0, 3085.0, 18.0], [17.0, 250.0, 100.0, 3329.0, 16.0], [29.0, 90.0, 70.0, 1937.0, 14.0], [44.3, 90.0, 48.0, 2085.0, 22.0], [10.0, 360.0, 215.0, 4615.0, 14.0], [18.0, 171.0, 97.0, 2984.0, 15.0], [26.0, 156.0, 92.0, 2585.0, 15.0], [13.0, 440.0, 215.0, 4735.0, 11.0], [24.0, 113.0, 95.0, 2372.0, 15.0], [13.0, 360.0, 170.0, 4654.0, 13.0], [24.0, 107.0, 90.0, 2430.0, 15.0], [28.8, 173.0, 115.0, 2595.0, 11.0], [37.0, 85.0, 65.0, 1975.0, 19.0], [32.9, 119.0, 100.0, 2615.0, 15.0], [37.7, 89.0, 62.0, 2050.0, 17.0], [16.0, 302.0, 140.0, 4141.0, 14.0], [22.0, 250.0, 105.0, 3353.0, 15.0], [18.0, 199.0, 97.0, 2774.0, 16.0], [19.0, 225.0, 100.0, 3630.0, 18.0], [38.0, 262.0, 85.0, 3015.0, 17.0], [28.4, 151.0, 90.0, 2670.0, 16.0], [21.5, 121.0, 110.0, 2600.0, 13.0], [16.0, 400.0, 170.0, 4668.0, 12.0], [18.5, 250.0, 110.0, 3645.0, 16.0], [20.2, 200.0, 88.0, 3060.0, 17.0], [26.0, 97.0, 78.0, 2300.0, 15.0], [33.5, 98.0, 83.0, 2075.0, 16.0], [18.0, 225.0, 105.0, 3121.0, 17.0], [28.0, 151.0, 90.0, 2678.0, 17.0], [18.0, 232.0, 100.0, 2945.0, 16.0], [24.0, 121.0, 110.0, 2660.0, 14.0], [23.0, 115.0, 95.0, 2694.0, 15.0], [32.4, 107.0, 72.0, 2290.0, 17.0], [12.0, 400.0, 167.0, 4906.0, 13.0], [13.0, 360.0, 175.0, 3821.0, 11.0], [27.0, 101.0, 83.0, 2202.0, 15.0], [13.0, 350.0, 145.0, 4055.0, 12.0], [33.5, 85.0, 70.0, 1945.0, 17.0], [16.5, 168.0, 120.0, 3820.0, 17.0], [18.5, 250.0, 98.0, 3525.0, 19.0], [16.0, 225.0, 105.0, 3439.0, 16.0], [14.0, 454.0, 220.0, 4354.0, 9.0], [20.2, 302.0, 139.0, 3570.0, 13.0], [34.3, 97.0, 78.0, 2188.0, 16.0], [18.0, 225.0, 95.0, 3785.0, 19.0], [11.0, 400.0, 150.0, 4997.0, 14.0], [30.0, 88.0, 76.0, 2065.0, 15.0], [21.0, 122.0, 86.0, 2226.0, 17.0], [26.0, 98.0, 79.0, 2255.0, 18.0], [14.0, 318.0, 150.0, 4077.0, 14.0], [23.5, 173.0, 110.0, 2725.0, 13.0], [38.0, 105.0, 63.0, 2125.0, 15.0], [12.0, 455.0, 225.0, 4951.0, 11.0], [38.1, 89.0, 60.0, 1968.0, 19.0], [24.5, 151.0, 88.0, 2740.0, 16.0], [16.0, 250.0, 100.0, 3781.0, 17.0], [31.0, 119.0, 82.0, 2720.0, 19.0], [41.5, 98.0, 76.0, 2144.0, 15.0], [26.0, 97.0, 46.0, 1835.0, 21.0], [34.0, 112.0, 88.0, 2395.0, 18.0], [27.0, 112.0, 88.0, 2640.0, 19.0], [27.0, 140.0, 86.0, 2790.0, 16.0], [18.0, 250.0, 88.0, 3021.0, 17.0], [28.0, 97.0, 75.0, 2155.0, 16.0], [33.0, 91.0, 53.0, 1795.0, 17.0], [28.0, 107.0, 86.0, 2464.0, 16.0], [21.1, 134.0, 95.0, 2515.0, 15.0], [33.8, 97.0, 67.0, 2145.0, 18.0], [17.0, 304.0, 150.0, 3672.0, 12.0], [34.4, 98.0, 65.0, 2045.0, 16.0], [14.0, 400.0, 175.0, 4385.0, 12.0], [27.2, 135.0, 84.0, 2490.0, 16.0], [13.0, 400.0, 190.0, 4422.0, 13.0], [39.0, 86.0, 64.0, 1875.0, 16.0], [43.4, 90.0, 48.0, 2335.0, 24.0], [36.1, 98.0, 66.0, 1800.0, 14.0], [26.6, 151.0, 84.0, 2635.0, 16.0], [27.0, 97.0, 60.0, 1834.0, 19.0], [24.0, 113.0, 95.0, 2278.0, 16.0], [25.8, 156.0, 92.0, 2620.0, 14.0], [15.0, 318.0, 150.0, 3399.0, 11.0], [23.0, 122.0, 86.0, 2220.0, 14.0], [13.0, 307.0, 130.0, 4098.0, 14.0], [26.0, 116.0, 75.0, 2246.0, 14.0], [20.2, 232.0, 90.0, 3265.0, 18.0], [31.6, 120.0, 74.0, 2635.0, 18.0], [44.0, 97.0, 52.0, 2130.0, 25.0], [20.2, 200.0, 85.0, 2965.0, 16.0], [29.0, 68.0, 49.0, 0.0, 20.0], [23.2, 156.0, 105.0, 2745.0, 17.0], [18.2, 318.0, 135.0, 3830.0, 15.0], [28.0, 120.0, 79.0, 2625.0, 19.0], [19.2, 305.0, 145.0, 3425.0, 13.0], [17.0, 231.0, 110.0, 3907.0, 21.0], [22.0, 122.0, 86.0, 2395.0, 16.0], [35.0, 72.0, 69.0, 1613.0, 18.0], [34.1, 86.0, 65.0, 1975.0, 15.0], [15.0, 350.0, 165.0, 3693.0, 12.0], [14.0, 455.0, 225.0, 4425.0, 10.0], [19.2, 267.0, 125.0, 3605.0, 15.0], [17.5, 305.0, 145.0, 3880.0, 13.0], [27.2, 141.0, 71.0, 3190.0, 25.0], [14.0, 455.0, 225.0, 3086.0, 10.0], [19.9, 260.0, 110.0, 3365.0, 16.0], [26.8, 173.0, 115.0, 2700.0, 13.0], [14.5, 351.0, 152.0, 4215.0, 13.0], [12.0, 350.0, 180.0, 4499.0, 13.0], [17.5, 250.0, 110.0, 3520.0, 16.0], [21.0, 199.0, 90.0, 3270.0, 15.0], [37.2, 86.0, 65.0, 2019.0, 16.0], [19.0, 250.0, 88.0, 3302.0, 16.0], [26.0, 91.0, 70.0, 1955.0, 21.0], [18.0, 250.0, 78.0, 3574.0, 21.0], [14.0, 351.0, 153.0, 4129.0, 13.0], [13.0, 351.0, 158.0, 4363.0, 13.0], [18.0, 250.0, 88.0, 3139.0, 15.0], [16.0, 318.0, 150.0, 4190.0, 13.0], [16.0, 400.0, 230.0, 4278.0, 10.0], [16.5, 351.0, 138.0, 3955.0, 13.0], [32.0, 91.0, 67.0, 1965.0, 16.0], [16.2, 163.0, 133.0, 3410.0, 16.0], [22.0, 121.0, 98.0, 2945.0, 15.0], [14.0, 304.0, 150.0, 3672.0, 12.0], [16.9, 350.0, 155.0, 4360.0, 15.0], [18.0, 232.0, 100.0, 3288.0, 16.0], [32.1, 98.0, 70.0, 2120.0, 16.0], [27.0, 151.0, 90.0, 2735.0, 18.0], [16.5, 350.0, 180.0, 4380.0, 12.0], [19.4, 318.0, 140.0, 3735.0, 13.0], [31.0, 71.0, 65.0, 1773.0, 19.0], [20.0, 114.0, 91.0, 2582.0, 14.0], [32.0, 83.0, 61.0, 2003.0, 19.0], [22.0, 232.0, 112.0, 2835.0, 15.0], [14.0, 340.0, 160.0, 3609.0, 8.0], [29.0, 97.0, 78.0, 1940.0, 15.0], [15.0, 429.0, 198.0, 4341.0, 10.0], [23.0, 120.0, 97.0, 2506.0, 15.0], [28.0, 97.0, 92.0, 2288.0, 17.0], [15.0, 350.0, 145.0, 4440.0, 14.0], [15.0, 350.0, 145.0, 4082.0, 13.0], [25.0, 116.0, 81.0, 2220.0, 17.0], [13.0, 318.0, 150.0, 3755.0, 14.0], [23.0, 350.0, 125.0, 3900.0, 17.0], [29.0, 90.0, 70.0, 1937.0, 14.0], [32.2, 108.0, 75.0, 2265.0, 15.0], [15.0, 302.0, 130.0, 4295.0, 15.0], [30.0, 79.0, 70.0, 2074.0, 20.0], [33.0, 91.0, 53.0, 1795.0, 18.0], [30.0, 97.0, 67.0, 1985.0, 16.0], [15.5, 400.0, 190.0, 4325.0, 12.0], [15.0, 390.0, 190.0, 3850.0, 9.0], [14.0, 440.0, 215.0, 4312.0, 9.0], [32.0, 144.0, 96.0, 2665.0, 14.0], [13.0, 350.0, 175.0, 4100.0, 13.0], [19.1, 225.0, 90.0, 4350.0, 19.0], [19.0, 156.0, 108.0, 2930.0, 16.0], [29.5, 98.0, 68.0, 2135.0, 17.0], [20.0, 156.0, 122.0, 2807.0, 14.0], [25.4, 183.0, 77.0, 3530.0, 20.0], [25.0, 121.0, 115.0, 2671.0, 14.0], [14.0, 318.0, 150.0, 4237.0, 15.0], [27.5, 134.0, 95.0, 2560.0, 14.0], [21.5, 80.0, 110.0, 2720.0, 14.0], [20.0, 97.0, 88.0, 2279.0, 19.0], [14.0, 302.0, 140.0, 4638.0, 16.0], [19.8, 0.0, 85.0, 2990.0, 18.0], [30.5, 98.0, 63.0, 2051.0, 17.0], [25.4, 168.0, 116.0, 2900.0, 13.0], [17.5, 258.0, 95.0, 3193.0, 18.0], [21.0, 231.0, 110.0, 3039.0, 15.0], [24.0, 116.0, 75.0, 2158.0, 16.0], [27.0, 97.0, 88.0, 2130.0, 15.0], [24.0, 119.0, 97.0, 2545.0, 17.0], [32.4, 108.0, 75.0, 2350.0, 17.0], [37.3, 91.0, 69.0, 2130.0, 15.0], [11.0, 350.0, 180.0, 3664.0, 11.0], [16.0, 250.0, 100.0, 3278.0, 18.0], [21.0, 200.0, 85.0, 2587.0, 16.0], [21.0, 120.0, 87.0, 2979.0, 20.0], [20.0, 130.0, 102.0, 3150.0, 16.0], [31.3, 120.0, 75.0, 2542.0, 18.0], [35.1, 81.0, 60.0, 1760.0, 16.0], [46.6, 86.0, 65.0, 2110.0, 18.0], [16.0, 231.0, 105.0, 3897.0, 19.0], [17.0, 305.0, 130.0, 3840.0, 15.0], [23.0, 120.0, 88.0, 2957.0, 17.0], [39.1, 79.0, 58.0, 1755.0, 17.0], [14.0, 302.0, 137.0, 4042.0, 15.0], [34.0, 108.0, 70.0, 2245.0, 17.0], [16.0, 318.0, 150.0, 4498.0, 15.0], [13.0, 302.0, 129.0, 3169.0, 12.0], [18.0, 250.0, 105.0, 3459.0, 16.0]]


def desconvertir(grafo, particiones):
    colores = ["#1976D2", "#E13918", "#28E118", "#C418E1", "#D6E118",
               "#E18518", "#18E1C5", "#6E18E1" "#18E1A8", "#18A5E1"]
    color = -1
    for mean in particiones:
        color = color+1
        for nodo in grafo["nodes"]:
            if nodo['id'] == mean[0]:
                nodo["color"] = colores[color]
    links = []
    for arista in grafo["links"]:
        try:
            if not arista["source"]["id"]:
                if arista["target"] == arista["source"]:
                    links.append(arista)
            elif arista["target"]["id"] == arista["source"]["id"]:
                if grafo["Ponderado"] == 1:
                    nuevolink = {
                        "source": arista["source"]["id"],
                        "target": arista["target"]["id"],
                        "weight": arista["weight"]
                    }
                else:
                    nuevolink = {
                        "source": arista["source"]["id"],
                        "target": arista["target"]["id"]
                    }
                links.append(nuevolink)
                
        except:
            if arista["target"] == arista["source"]:
                links.append(arista)

    grafo["links"] = links
    return grafo


# funcion auxiliar
def FindColMinMax(items):
    n = len(items[0])
    minima = [sys.maxsize for i in range(n)]
    maxima = [-sys.maxsize - 1 for i in range(n)]

    for item in items:
        for f in range(len(item)):
            if(item[f] < minima[f]):
                minima[f] = item[f]

            if(item[f] > maxima[f]):
                maxima[f] = item[f]

    return minima, maxima


def EuclideanDistance(x, y):
    S = 0  # La suma de las diferencias al cuadrado de los elementos
    for i in range(len(x)):
        S += math.pow(x[i]-y[i], 2)

    return math.sqrt(S)  # La ra??z cuadrada de la suma


def InitializeMeans(items, k, cMin, cMax):
    # Inicializar 'means' a n??meros aleatorios entre
    # el m??nimo y m??ximo de cada columna/caracter??stica

    f = len(items[0])  # nn??mero de caracter??sticas
    means = [[0 for i in range(f)] for j in range(k)]

    for mean in means:
        for i in range(len(mean)):
            # Establecer valor a un flotador aleatorio
            # (agregando +-1 para evitar una colocaci??n amplia de una media)
            mean[i] = uniform(cMin[i]+1, cMax[i]-1)

    return means


def UpdateMean(n, mean, item):
    for i in range(len(mean)):
        m = mean[i]
        m = (m*(n-1)+item[i])/float(n)
        mean[i] = round(m, 3)

    return mean


def FindClusters(means, items):
    clusters = [[] for i in range(len(means))]  # inicializar clusters

    for item in items:
        # Clasificar elemento en un grupo
        index = Classify(means, item)

        # A??adir elemento al cl??ster
        clusters[index].append(item)

    return clusters


# funciones mas importantes
def Classify(means, item):
    # Clasificar elemento mean con distancia m??nima

    minimum = sys.maxsize
    index = -1

    for i in range(len(means)):
        # Encontrar la distancia del elemento a mean
        dis = EuclideanDistance(item, means[i])

        if(dis < minimum):
            minimum = dis
            index = i

    return index


def CalculateMeans(k, items, maxIterations=200):
    # Encuentra los m??nimos y m??ximos de las columnas
    cMin, cMax = FindColMinMax(items)

    # Inicializar medios en puntos aleatorios
    means = InitializeMeans(items, k, cMin, cMax)

    # Inicialice los cl??steres, la matriz que se mantendr??
    # el n??mero de art??culos en una clase
    clusterSizes = [0 for i in range(len(means))]

    # Una matriz para contener el grupo en el que se encuentra un elemento
    belongsTo = [0 for i in range(len(items))]

    # Calculamos means
    for e in range(maxIterations):
        # si no hay cambios salimos
        noChange = True
        for i in range(len(items)):
            item = items[i]

            # Clasificar elemento en un grupo y actualizar el
            # means correspondientes.
            index = Classify(means, item)

            clusterSizes[index] += 1
            means[index] = UpdateMean(clusterSizes[index], means[index], item)

            # Item cambio?
            if(index != belongsTo[i]):
                noChange = False

            belongsTo[i] = index

        # SI NADA CAMBIO SALIMOS
        if(noChange):
            break

    return means


def CalculateLossValue(clusters, means):

    m = len(clusters)
    totalLoss = 0
    for i in range(len(clusters)):
        for item in clusters[i]:
            loss = EuclideanDistance(item, means[i])
            totalLoss += math.pow(loss, 2)

    return totalLoss / m


# PRINCIPAL
def ejecutarQclustering(grafo):
    items = convertir(grafo)
    # Empezamos a contar el tiempo
    inicial = time.time()
    lossValues = []
    means = []  # PAra evitar errores
    for k in range(1, 10):
        means = CalculateMeans(k, items)
        clusters = FindClusters(means, items)
        lossValue = CalculateLossValue(clusters, means)
        lossValues.append(lossValue)
        print(math.sqrt(lossValue))
    # dejamos de contar el tiempo
    final = time.time()
    grafo["tiempo"] = final-inicial
    plt.plot(lossValues)
    plt.xlabel('k')
    plt.ylabel('perdida')
    plt.grid(True)
    plt.show()
    return desconvertir(grafo, means)
