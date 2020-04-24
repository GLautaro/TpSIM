import math
import statistics as stats
import numpy as np
from Modulos.Utils import Truncate

def FuncionAcumuladaExponencial(x, valor_lambda):
    '''La función devuelve el valor de la función acumulada para la distribución exponencial valuada en X
       Parámetros: x: variable a valuar la función
                   valor_lambda: valor del lambda calculado para la serie'''
    return 1-math.exp(-valor_lambda*x)

def FuncionDensidadNormal(x, media, desviacion_estandar):
    '''La función devuelve el valor de la función de densidad para la distribución normal valuada en X
       Parámetros: x: variable a valuar la función
                   media: media calculada para la serie
                   desviacion_estandar: desviación estandar calculada para la serie'''
    return (math.exp(-0.5*((x-media)/desviacion_estandar)**2))/(desviacion_estandar*math.sqrt(2*math.pi))

def FuncionAcumuladaUniforme(a, b, x):
    '''La función devuelve el valor de la función acumulada para la distribución uniforme valuada en X
        Parámetros: x: variable a valuar la función
                    a: extremo superior
                    b: extremo inferior'''
    return (x-a)/(b-a)

def ProbabilidadAcumuladaExponencial(desde, hasta, valor_lambda):
    '''La función devuelve el valor de la probabilidad acumulada para la distribución Exponencial
       Parámetros: desde: valor inicial del intervalo
                   hasta: valor final del intervalo
                   valor_lambda: valor del lambda calculado para la serie'''
    return FuncionAcumuladaExponencial(hasta, valor_lambda) - FuncionAcumuladaExponencial(desde, valor_lambda)

def ProbabilidadAcumuladaNormal(desde, hasta, a, b):
    '''La función devuelve el valor de la probabilidad acumulada para la distribución Exponencial
        Parámetros: desde: valor inicial del intervalo
                    hasta: valor final del intervalo
                    a: extremo superior
                    b: extremo inferior'''
    return FuncionAcumuladaUniforme(a, b, hasta) - FuncionAcumuladaUniforme(a, b, desde)

def FrecuenciasEsperadas(tamaño_muestra, intervalos, tipoDistribucion, media, desviacion_estandar, a, b):
    '''La función calcula la frecuencia esperada para cada intervalo según el tipo de distribución elegida
       Parámetros: tamaño_muestra: entero que representa la cantidad de elementos de la serie
                   intervalos: intervalos Dict<str, extremos> Diccionario que utiliza como clave la representacion del intervalo
                   tipoDistribucion: entero que representa el tipo de distribución elegida como hipótesis nula (0=uniforme, 1=exponencial, 2=normal)
                   media: media calculada para la serie
                   desviacion_estandar: desviacion estandar calculada para la serie
                   a: valor minimo de la serie
                   b: valor maximo de la serie
       Return: lista con frecuencias esperadas'''
    
    frec_esp_arr = []
    valor_lambda = Truncate(1/media, 7)

    for i in intervalos:
        intervalo = intervalos[i]
        desde, hasta = intervalo[0], intervalo[1]

        if tipoDistribucion == 0:
          prob = ProbabilidadAcumuladaNormal(desde, hasta, a, b)

        elif tipoDistribucion == 1:
          prob = ProbabilidadAcumuladaExponencial(desde, hasta, valor_lambda)
        
        elif tipoDistribucion == 2:
          marca_clase = (desde+hasta)/2
          prob = FuncionDensidadNormal(marca_clase, media, desviacion_estandar)*(hasta-desde)
        
        frec_esp = Truncate(prob*tamaño_muestra, 4)
        
        frec_esp_arr.append(frec_esp)
    
    return frec_esp_arr

def testFrecuenciasEsperadasExponencial():
    arr = [0.10, 0.25, 1.53, 2.83, 3.50, 4.14, 5.65, 6.96, 7.19, 8.25,1.20, 5.24, 4.75, 3.96, 2.21, 3.15, 2.53, 1.16, 0.32, 0.90, 0.87, 1.34, 1.87, 2.91, 0.71, 1.69, 0.69, 0.55, 0.43, 0.26]
    intervalos = {'0 - 1': [0, 1], '1 - 2': [1, 2], '2 - 3': [2, 3], '3 - 4': [3, 4], '4 - 5': [4, 5], '5 - 6': [5, 6], '6 - 7': [6, 7], '7 - 8': [7, 8], '8 - 9': [8, 9], '9 - 10': [9, 10]}
    tipoDistribucion = 1
    tamaño_muestra = 30
    a, b = min(arr), max(arr)
    media = stats.mean(arr)
    print('Media:', media)
    desviacion_estandar = np.std(arr, ddof=1)
    frec_esp = FrecuenciasEsperadas(tamaño_muestra, intervalos, tipoDistribucion, media, desviacion_estandar, a, b)
    print(frec_esp)

def testFrecuenciasEsperadasNormal():
    arr = [1.56, 2.21, 3.15, 4.61, 4.18, 5.20, 6.94, 7.71, 5.15, 6.76, 7.28, 4.23, 3.21, 2.75, 4.69, 5.86, 6.25, 4.27, 4.91, 4.78, 2.46, 3.97, 5.71, 6.19, 4.20, 3.48, 5.83, 6.36, 5.90, 5.43]
    intervalos = {'0 - 1': [0, 1], '1 - 2': [1, 2], '2 - 3': [2, 3], '3 - 4': [3, 4], '4 - 5': [4, 5], '5 - 6': [5, 6], '6 - 7': [6, 7], '7 - 8': [7, 8], '8 - 9': [8, 9], '9 - 10': [9, 10]}
    media = stats.mean(arr)
    print('Media:', media)
    desviacion_estandar = np.std(arr, ddof=1)
    print('Desv estandar: ', desviacion_estandar)
    tipoDistribucion = 2
    tamaño_muestra = 30
    a, b = min(arr), max(arr)
    frec_esp = FrecuenciasEsperadas(tamaño_muestra, intervalos, tipoDistribucion, media, desviacion_estandar, a, b)
    print(frec_esp)

def testFrecuenciasEsperadasUniforme():
    arr = [0.15, 0.22, 0.41, 0.65, 0.84, 0.81, 0.62, 0.45, 0.32, 0.07, 0.11, 0.29, 0.58, 0.73, 0.93, 0.97, 0.79, 0.55, 0.35, 0.09, 0.99, 0.51, 0.35, 0.02, 0.19, 0.24, 0.98, 0.10, 0.31, 0.17]
    intervalos = {'0.0 - 0.2': [0.0, 0.2], '0.2 - 0.4': [0.2, 0.4], '0.4 - 0.6': [0.4, 0.6], '0.6 - 0.8': [0.6, 0.8], '0.8 - 1.0': [0.8, 1.0]}
    media = stats.mean(arr)
    desviacion_estandar = np.std(arr, ddof=1)
    tipoDistribucion = 0
    tamaño_muestra = 30
    a, b = min(arr), max(arr)
    print(a,b)
    frec_esp = FrecuenciasEsperadas(tamaño_muestra, intervalos, tipoDistribucion, media, desviacion_estandar, a, b)
    print(frec_esp)


        