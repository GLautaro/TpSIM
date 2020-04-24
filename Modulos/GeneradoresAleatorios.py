import random
import numpy as np
from Modulos.Utils import Truncate

def ListaAleatoriaNativa(n, inferior, superior, s=None):
    if superior == 1:
        superior = 1.0001
    if s is not None:
        random.seed(s)
    #La funcion aleatoria se parametriza con el rango [0, 1.00001] para generar numeros aleatorios menores o iguales a uno
    #por algunos decimales, que luego son truncados mediante la funcion
    numbers_array = list([Truncate(random.uniform(inferior,superior), 4) for i in range(n)])
    return numbers_array

'''La función genera una muestra de n números aleatorios con distribución exponencial negativa
    Parametros: n: tamaño de la muestra, media: valor de la media
    Si se ingresa un lambda negativo la funcion genera números comprendidos entre infinito negativo y cero. 
    Si se ingresa un lambda positivo la funcion genera números que se encuentran entre cero e infinito
    Retorna list : Lista con los números generados
'''
def distribucionExponencial(n, media):
    valor_lambda= 1 / media
    return list([Truncate(random.expovariate(valor_lambda), 4) for i in range(n)])

'''La función genera una lista de n números aleatorios con distribución normal usando el método de Box-Muller
    Parámetros: n: tamaño de la muestra, mu: media, sigma: desviación estándar
    Retorna list: lista con los números generados
'''
def distribucionNormal(n, mu, sigma):
    return list([Truncate(random.gauss(mu, sigma),4) for i in range(n)])

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
