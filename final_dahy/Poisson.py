import math
import random

def poisson(media):
    p = 1
    x = -1
    a = math.exp(-media)
    u = random.random()
    p = p * u
    x = x + 1
    while (p >= a):
        u = random.random()
        p = p * u
        x = x + 1
    return x

for i in range(5):
    print(poisson(2))



