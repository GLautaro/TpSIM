import math
import statistics as stats

def FuncionAcumuladaExponencial(x, valor_lambda):
    '''La función devuelve el valor de la función acumulada exponencial valuada en X
       Parámetros: x: variable a valuar la función
                   valor_lambda: valor del lambda calculado para la serie'''
    return 1-math.exp(-valor_lambda*x)

def ProbabilidadAcumulada(desde, hasta, valor_lambda):
    '''La función devuelve el valor de la probabilidad acumulada
       Parámetros: desde: valor inicial del intervalo
                   hasta: valor final del intervalo
                   valor_lambda: valor del lambda calculado para la serie'''
    return FuncionAcumuladaExponencial(hasta, valor_lambda) - FuncionAcumuladaExponencial(desde, valor_lambda)

def FrecuenciasEsperadas(tamaño_muestra, intervalos, tipoDistribucion, media):
    '''La función calcula la frecuencia esperada para cada intervalo según el tipo de distribución elegida
       Parámetros: tamaño_muestra: entero que representa la cantidad de elementos de la serie
                   intervalos: intervalos Dict<str, extremos> Diccionario que utiliza como clave la representacion del intervalo
                   tipoDistribucion: entero que representa el tipo de distribución elegida como hipótesis nula
                   media: media calculada para la serie
       Return: lista con frecuencias esperadas'''
    if tipoDistribucion == 0:
        pass
    elif tipoDistribucion == 1:
        frec_esp_arr = []
        valor_lambda = 1/media
        print('Lambda: ', valor_lambda)
        for i in intervalos:
            intervalo = intervalos[i]
            desde, hasta = intervalo[0], intervalo[1]
            prob_acum = ProbabilidadAcumulada(desde, hasta, valor_lambda)
            print('Probabilidad acumulada: ', prob_acum)
            frec_esp = prob_acum*tamaño_muestra
            frec_esp_arr.append(frec_esp)
        return frec_esp_arr
    elif tipoDistribucion == 2:
        pass

def testFrecuenciasEsperadas():
    arr = [0.10, 0.25, 1.53, 2.83, 3.50, 4.14, 5.65, 6.96, 7.19, 8.25,1.20, 5.24, 4.75, 3.96, 2.21, 3.15, 2.53, 1.16, 0.32, 0.90, 0.87, 1.34, 1.87, 2.91, 0.71, 1.69, 0.69, 0.55, 0.43, 0.26]
    intervalos = {'0 - 1': [0, 1], '1 - 2': [1, 2], '2 - 3': [2, 3], '3 - 4': [3, 4], '4 - 5': [4, 5], '5 - 6': [5, 6], '6 - 7': [6, 7], '7 - 8': [7, 8], '8 - 9': [8, 9], '9 - 10': [9, 10]}
    tipoDistribucion = 1
    tamaño_muestra = 30
    media = stats.mean(arr)
    print('Media:', media)
    frec_esp = FrecuenciasEsperadas(tamaño_muestra, intervalos, tipoDistribucion, media)
    print(frec_esp)

        