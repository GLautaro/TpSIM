import random
import numpy as np
from math import trunc


def Truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

def ListaAleatoriaNativa(n, s=None):
    if s is not None:
        random.seed(s)
    numbers_array = list(map(lambda x: Truncate(x, 4), [random.random() for i in range(n)]))
    return numbers_array

def ListaAleatoriaCongruencialLineal(n,x,k,g,c):
    numeros_generados = []
    a = 1 + 4*k
    m = 2**g
    for i in range(n):
        x = (a*x + c)%m
        y = x/(m-1)
        numeros_generados.append(Truncate(y, 4))
    
    return numeros_generados

'''La función implementa el método Congruencial Multiplicativo
    Parametros: n: tamaño de la muestra, x: Semilla, k: entero para obtener la constante multiplicativa, 
                g: entero para obtener el módulo
    Retorna list : Lista con los números generados
'''
def ListaAleatoriaCongruencialMultiplicativo(n, x, k, g):
    numeros_generados = []
    a = 3 + 8*k
    m = 2**g
    for i in range(n):
        x = ((a*x)%m)
        y = x/(m-1)
        numeros_generados.append(Truncate(y, 4))

    return numeros_generados

def ListaNumerosAleatorios(opcion_seleccionada, n, x, k, g, c):
        if opcion_seleccionada == 0:
            return ListaAleatoriaCongruencialLineal(n,x,k,g,c)
        elif opcion_seleccionada == 1:
            return ListaAleatoriaCongruencialMultiplicativo(n,x,k,g)
        
        elif opcion_seleccionada == 2:
            if x < 0:
                return ListaAleatoriaNativa(n)
            else:
                return ListaAleatoriaNativa(n,x)
