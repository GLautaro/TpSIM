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
    return intervalos

def CalcularPinosTirada(prob, nro_aleatorio, primera_tirada = True):
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

    return indice + 7 if primera_tirada else indice

def CalcularCantidadArchivos(prob, nro_aleatorio):
    len_lista = len(prob)
    nro_aleatorio = nro_aleatorio * 100
    indice = 0
    for i in range(len_lista - 1):
        if i == len_lista - 2:
            if prob[i] <= nro_aleatorio <= prob[i + 1]:
                indice = i
                break
        if prob[i] <= nro_aleatorio < prob[i + 1]:
            indice = i
            break
    if indice == 2:
        return 2000
    elif indice == 1:
        return 1500
    elif indice == 0:
        return 1000
    else:
        raise Exception("El vector de probabilidades acumuladas no se corresponde con los parametros necesarios para la simulacion")
""" 
def CalcularPinosSegundaTirada(probabilidades,nro_aleatorio,pinos_primera):
    len_lista = len(probabilidades)
    nro_aleatorio = nro_aleatorio * 100
    indice = 0
    for i in range(len_lista - 1):
        if i == len_lista - 2:
            if nro_aleatorio >= prob[i] and nro_aleatorio <= prob[i + 1]:
            indice = i
            break
        if nro_aleatorio >= probabilidades[i] and nro_aleatorio < probabilidades[i + 1]:
            indice = 1
            break

    return indice """