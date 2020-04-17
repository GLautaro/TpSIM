import random
import numpy as np
from Modulos.Utils import Truncate

def ListaAleatoriaNativa(n, s=None):
    if s is not None:
        random.seed(s)
    #La funcion aleatoria se parametriza con el rango [0, 1.00001] para generar numeros aleatorios mayores o iguales a uno
    #por algunos decimales, que luego son truncados mediante la funcion
    numbers_array = list([Truncate(random.uniform(0,1.0001), 4) for i in range(n)])
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
