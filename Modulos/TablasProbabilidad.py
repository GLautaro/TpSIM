def CrearProbabilidadesAcumuladas(prob):
    v = [0] * (len(prob) + 1)
    for i in range(len(prob)):
        v[i + 1] = v[i] + prob[i]
    return v

def CrearIntervalos(prob):
    prob_acumuladas = CrearProbabilidadesAcumuladas(prob)
    intervalos = []
    for i in range(len(prob_acumuladas) - 1):
        intervalos.append(str(prob_acumuladas[i]) + " - " + str(prob_acumuladas[i + 1]))
    print(intervalos)
    return intervalos

def CalcularPinosPrimeraTirada(prob, nro_aleatorio):
    len_lista = len(prob)
    nro_aleatorio = nro_aleatorio * 100
    indice = 0
    for i in range(len_lista - 1):
        if i == len_lista - 2:
            if nro_aleatorio >= prob[i] and nro_aleatorio <= prob[i + 1]:
                indice = i
                break
        if nro_aleatorio >= prob[i] and nro_aleatorio < prob[i + 1]:
            indice = i
            break

    return indice + 7

def CalcularPinosSegundaTirada(probabilidades,nro_aleatorio,pinos_primera):
    pass