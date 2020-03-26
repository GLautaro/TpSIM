# Modulo utilizado para desarrollar funciones referidas al manejo de numeros

from random import random


def generate_numbers(n):
    numbers_array = list(map(lambda x: round(x, 4), [random() for i in range(n)]))
    return numbers_array