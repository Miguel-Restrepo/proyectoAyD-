from __future__ import division
import numpy as np
#import matplotlib.pyplot as plt
import numpy.linalg as la
import copy
#from collections import Sequence
#from itertools import chain, count
#from scipy.linalg import block_diag
from typing import Any

# funciones preliminares
def trinv(matrix):
    tri = np.trace(la.inv(matrix))
    return tri

def permutation_matrix(n):
    rr = range(n)
    np.random.shuffle(rr)
    P = np.take(np.eye(n), rr, axis=0)
    return  P

#Ordenar filas y columnas
def select_mat(matrix, index_row, index_column):
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
        yield [ collection ]
        return
    first = collection[0]
    for smaller in partition(collection[1:]):# insertar el primero en cada subconjunto
        for n, subset in enumerate(smaller):
            yield smaller[:n] + [[ first ] + subset]  + smaller[n+1:]
        # primero en su propio subconjunto
        yield [ [ first ] ] + smaller

def select_from_list(list, indices):
    list_select = [list[i] for i in indices]
    return list_select

# encontrar un par Q,W
# encontrar entre Q y W el mas lejano
# in Q to W
# prerequisito: W y Q deben ser listas de listas

def Find_Far_Element(SS, F, WW, QQ):
    u = QQ[0]  
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

# encontrar particion pendiente
# V es todos los puntos incluido los fusionados
# V tiene una longitud entre n y 2
def PENDENT_PAIR(SS, VV, F):
    V_ = copy.copy(VV)
    rnd_pattern = np.random.permutation(len(V_))#arranca en uno aleatorio
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

#Algoritmo como tal

def QUEYRANNE(SS, F):
    dim, _ = SS.shape
    V = range(dim)  # espacio de nodos en cada particion completa
    C = []  # conjunto actualizado
    while len(V) >= 3:
        W = copy.deepcopy(V)
        a, b = PENDENT_PAIR(SS, W, F)  #busca un par pendiente en V, F
        if type(b) == int:
            C.append([b])
        else:
            C.append(b)
        fus = fuse(a, b)  
        V.append(fus)
        if ismember(a, V) is True and ismember(b, V) is True:
            V.remove(a)
            V.remove(b)
    for subset in V:
        if type(subset) == int:
            C.append([subset])
        else:
            C.append(subset)
    #  al tener la lista de candidatos devolvemos el mejor
    max_value = -np.Inf
    subset_opt = []
    cluster_max = 0
    valor_particion = 0
    for subset in C:
        cluster_value = F(SS, subset)
        subset_value = cluster_value + F(SS, diff(range(dim), subset))
        if subset_value > max_value:
            subset_opt = subset
            valor_particion = subset_value
            cluster_max = cluster_value
            max_value = subset_value
    return subset_opt, valor_particion, cluster_max