from Modulos.Utils import Truncate, CrearDataFrame, GenerarExcel
import Modulos.TablasProbabilidad as tablas
import pandas as pd
import random 
import os

def SimulacionBowling(vector_primera_bola,
                      vector_segunda_bola_7,
                      vector_segunda_bola_8,
                      vector_segunda_bola_9,
                      it,ron,
                      puntaje_objetivo, punt_10_prim,punt_10_seg,
                      mostrar_ronda_desde,mostrar_ronda_cantidad,
                      mostrar_iteracion_desde, mostrar_iteracion_cantidad
                      ):
    int_pr = tablas.CrearProbabilidadesAcumuladas(vector_primera_bola)
    int_seg_7 = tablas.CrearProbabilidadesAcumuladas(vector_segunda_bola_7)
    int_seg_8 = tablas.CrearProbabilidadesAcumuladas(vector_segunda_bola_8)
    int_seg_9 = tablas.CrearProbabilidadesAcumuladas(vector_segunda_bola_9)
    
    cant_exitos = 0
    iteraciones = []
    for i in range(it):
        puntajeTotal = 0
        ronda_datos = [str(i + 1), "Falló"]
        for j in range(ron):
            puntajeRonda = 0
            rand_tirada_1 = Truncate(random.uniform(0, 1.00001), 4)
            cant_pinos = tablas.CalcularPinosTirada(int_pr, rand_tirada_1)
            rand_tirada_2 = Truncate(random.uniform(0, 1.00001), 4)
            cant_pinos_seg = 0
            if(cant_pinos == 7):                
                cant_pinos_seg = tablas.CalcularPinosTirada(int_seg_7, rand_tirada_2, primera_tirada=False)
            elif(cant_pinos == 8):
                cant_pinos_seg = tablas.CalcularPinosTirada(int_seg_8, rand_tirada_2, primera_tirada=False)
            elif(cant_pinos == 9):
                cant_pinos_seg = tablas.CalcularPinosTirada(int_seg_9, rand_tirada_2, primera_tirada=False)

            if(cant_pinos == 10):
                puntajeRonda = punt_10_prim
            elif((cant_pinos + cant_pinos_seg) == 10):
                puntajeRonda = punt_10_seg
            else:
                puntajeRonda = cant_pinos + cant_pinos_seg
            
            puntajeTotal += puntajeRonda
            if j + 1 >= mostrar_ronda_desde and (j + 1) - mostrar_ronda_desde < mostrar_ronda_cantidad or (j + 1) == ron:
                ronda_datos.extend([rand_tirada_1, cant_pinos, rand_tirada_2, cant_pinos_seg, puntajeRonda, puntajeTotal])

        if (i + 1) >= mostrar_iteracion_desde and (i + 1) - mostrar_iteracion_desde < mostrar_iteracion_cantidad or (i + 1) == it:
            if puntajeTotal >= puntaje_objetivo:
                ronda_datos[1] = "Éxito"
            iteraciones.append(ronda_datos)
         
        if puntajeTotal >= puntaje_objetivo:
            cant_exitos += 1
    
    probabilidad_exito = cant_exitos / it
    return CrearDataFrame(mostrar_ronda_cantidad + 1 if ron - mostrar_ronda_desde - mostrar_ronda_cantidad == 0 else mostrar_ronda_cantidad, mostrar_ronda_desde, iteraciones, ron),probabilidad_exito

def testSimulacionMonte():
    import os
    import Modulos.Utils as u
    sim = SimulacionBowling([12,15,18,55],
                     [2,10,45,43],
                      [4,26,76],
                      [6,94],
                      5,10,
                      120, 20,15,
                      1,2, #Rondas desde/cantidad
                      3,1
                      )
    nom = "file.xlsx"
    u.GenerarExcel({"Simulacion":sim},nom)
    os.startfile(nom)
    return sim

if __name__ == "__main__":
    testSimulacionMonte()