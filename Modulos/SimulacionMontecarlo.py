from Modulos import TablasProbabilidad as tablas
from Modulos.Utils import Truncate, CrearDataFrame
import pandas as pd
import random 


def SimulacionBowling(vector_primera_bola,
                      vector_segunda_bola_7,
                      vector_segunda_bola_8,
                      vector_segunda_bola_9,
                      it,ron,
                      puntaje_objetivo, punt_10_prim,punt_10_seg,
                      mostrar_desde,mostrar_cantidad
                      ):
    int_pr = tablas.CrearProbabilidadesAcumuladas(vector_primera_bola)
    int_seg_7 = tablas.CrearProbabilidadesAcumuladas(vector_segunda_bola_7)
    int_seg_8 = tablas.CrearProbabilidadesAcumuladas(vector_segunda_bola_8)
    int_seg_9 = tablas.CrearProbabilidadesAcumuladas(vector_segunda_bola_9)
    
    cant_exitos = 0
    df = pd.DataFrame(columns=['Exito',])
    iteraciones = []
    for i in range(it):
        iteracion = "It º" + str(i)
        puntajeTotal = 0
        ronda_datos = [i]
        for j in range(ron):
            ronda = "Ronda " + str(j)
            tirada1 = ronda + " tirada 1"
            tirada2 = ronda + " tirada 2"
            puntaje = 0
            rand_tirada_1 = Truncate(random.uniform(0,1.00001), 4)
            cant_pinos = tablas.CalcularPinosTirada(int_pr, rand_tirada_1)
            rand_tirada_2 = Truncate(random.uniform(0,1.00001), 4)         

            if(cant_pinos == 7):                
                 cant_pinos_seg = tablas.CalcularPinosTirada(int_seg_7, rand_tirada_2, primera_tirada=False)
            elif(cant_pinos==8):
                cant_pinos_seg = tablas.CalcularPinosTirada(int_seg_8, rand_tirada_2, primera_tirada=False)
            else:
                 cant_pinos_seg = tablas.CalcularPinosTirada(int_seg_9, rand_tirada_2, primera_tirada=False)
            if(cant_pinos == 10):
                puntaje = punt_10_prim
            elif((cant_pinos + cant_pinos_seg) == 10):
                puntaje = punt_10_seg
            else:
                puntaje = cant_pinos + cant_pinos_seg

            puntajeTotal += puntaje

            if(i+1 >= it-1):
                ronda_datos.extend([rand_tirada_1, cant_pinos, rand_tirada_2, cant_pinos_seg, puntajeTotal])

        if(len(ronda_datos)>1):
            iteraciones.append(ronda_datos)
            
        if puntajeTotal >= puntaje_objetivo:
            cant_exitos += 1
    
    probabilidad_exito = cant_exitos / it
    
    return CrearDataFrame(ron, iteraciones)

def testSimulacionMonte():
    return SimulacionBowling([1,2,3,4,4],
                     [1,2,3,4,4],
                      [1,2,3,4,4],
                      [1,2,3,4,4],
                      5,5,
                      120, 125,222,
                      2,2
                      )