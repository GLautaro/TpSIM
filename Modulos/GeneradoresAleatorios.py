from random import random
import numpy as np

def ListaAleatoriaNativa(n):
    numbers_array = list(map(lambda x: round(x, 4), [random() for i in range(n)]))
    return numbers_array

def ListaAleatoriaCongruenciaLineal(n):
    pass

def ListaAleatoriaCongruenciaMultiplicativa(n):
    k=2
    x = 17 #Semilla
    g = np.log2(n)+2
    a = 3 + 8*k #Constante Multiplicativa
    m = 2**g #Módulo
    result = []
    for i in range(n):
        z = a*x
        x = (z%m)
        y = x/(m-1)
        result.append(round(y, 4))
        
    return result



