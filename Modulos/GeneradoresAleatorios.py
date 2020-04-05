from random import random
import numpy as np

def ListaAleatoriaNativa(n):
    numbers_array = list(map(lambda x: round(x, 4), [random() for i in range(n)]))
    return numbers_array

def ListaAleatoriaCongruencialLineal(n,x,a,m,c):
    numeros_generados = []
    for i in range(n):
        x = (a*x + c)%m
        y = x/(m-1)
        numeros_generados.append(round(y, 4))
    
    return numeros_generados

'''La función implementa el método Congruencial Multiplicativo
    Parametros: n: tamaño de la muestra, x: Semilla, a: Constante Multiplicativa, m: Módulo
    Retorna list : Lista con los números generados
'''
def ListaAleatoriaCongruencialMultiplicativo(n,x,a,m):
    numeros_generados = []
    for i in range(n):
        x = ((a*x)%m)
        y = x/(m-1)
        numeros_generados.append(round(y, 4))

    return numeros_generados

def ListaNumerosAleatorios(opcion_seleccionada, n, x,a ,m, c):
        if opcion_seleccionada == 0:
            return ListaAleatoriaCongruencialLineal(n,x,a,m,c)
        elif opcion_seleccionada == 1:
            return ListaAleatoriaCongruencialMultiplicativo(n,x,a,m)
        elif opcion_seleccionada == 2:
            return ListaAleatoriaNativa(n)
