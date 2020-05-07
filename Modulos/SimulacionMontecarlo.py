from Modulos import TablasProbabilidad as tablas
from Modulos.Utils import Truncate
import pandas as pd
import random 


def SimulacionBowling(vector_primera_bola,
                      vector_segunda_bola_7,
                      vector_segunda_bola_8,
                      vector_segunda_bola_9,
                      it,ron,
                      punt_objetivo, punt_10_prim,punt_10_seg
                      mostrar_desde,mostrar_cantidad
                      )
    int_pr = tablas.CrearProbabilidadesAcumuladas(vector_primera_bola)
    int_seg_7 = tablas.CrearProbabilidadesAcumuladas(vector_segunda_bola_7)
    int_seg_8 = tablas.CrearProbabilidadesAcumuladas(vector_segunda_bola_8)
    int_seg_9 = tablas.CrearProbabilidadesAcumuladas(vector_segunda_bola_9)
    
    cant_exitos = 0
    df = pd.DataFrame(columns=['Exito',])
    for i in range(it):
        iteracion = "It º" + str(i)
        for j in range(ron):
            ronda = "Ronda " + str(j)
            tirada1 = ronda + " tirada 1"
            tirada2 = ronda + " tirada 2"

            puntaje = 0
            ran = Truncate(random.uniform(0,1.00001), 4)
            cant_pinos = tablas.CalcularPinosTirada(int_pr, ran)


            if puntaje >= puntaje_objetivo:
                cant_exitos += 1

    probabilidad_exito = cant_exitos / it
