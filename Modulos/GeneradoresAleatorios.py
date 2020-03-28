from random import random
import numpy as np

def ListaAleatoriaNativa(n):
    numbers_array = list(map(lambda x: round(x, 4), [random() for i in range(n)]))
    return numbers_array



def ListaAleatoriaCongruencialLineal(n):
    pass

'''La función implementa el método Congruencial Multiplicativo
    Parametros: n : int Periodo máximo 
    Retorna list : Lista con los números generados
'''
def ListaAleatoriaCongruencialMultiplicativo(n):
    k=2
    x = 17 #Semilla
    a = 3 + 8*k #Constante Multiplicativa
    m = 2**(np.log2(n)+2) #Módulo -- La variable g se obtiene apartir del periodo máximo ingresado
    numeros_generados = []

    for i in range(n):
        x = ((a*x)%m)
        y = x/(m-1)
        numeros_generados.append(round(y, 4))
        
    return numeros_generados

def ListaNumerosAleatorios(n, opcion_seleccionada):
        if opcion_seleccionada == 0:
            return ListaAleatoriaCongruencialLineal(n)
        elif opcion_seleccionada == 1:
            return ListaAleatoriaCongruencialMultiplicativo(n)
        elif opcion_seleccionada == 2:
            return ListaAleatoriaNativa(n)

