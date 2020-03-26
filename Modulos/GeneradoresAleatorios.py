from random import random

def ListaAleatoriaNativa(n):
    numbers_array = list(map(lambda x: round(x, 4), [random() for i in range(n)]))
    return numbers_array

def ListaAleatoriaCongruenciaLineal(n):
    pass

def ListaAleatoriaCongruenciaMultiplicativa(n):
    pass


