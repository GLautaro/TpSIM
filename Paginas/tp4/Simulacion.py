# Importacion de modulos de terceros
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import Modulos.TablasProbabilidad as tablas

def LoadPage():
    st.title('🔢Simulación de Montecarlo - Bowling')
    st.markdown('Ingrese los parametros requeridos y luego pulse "Iniciar Simulación" para comenzar con la simulación.')

    #Probabilidades de la primera bola. Genera un vector de probabilidades
    st.subheader('📊Probabilidades de la Primera bola:')
    bola1_7pinos = st.number_input('Probabilidad de tirar 7 pinos (%):', min_value=0.0, max_value=100.0, value=12.0)
    bola1_8pinos = st.number_input('Probabilidad de tirar 8 pinos (%):', min_value=0.0, max_value=100.0, value=15.0)
    bola1_9pinos = st.number_input('Probabilidad de tirar 9 pinos (%):', min_value=0.0, max_value=100.0, value=18.0)
    bola1_10pinos = st.number_input('Probabilidad de tirar 10 pinos (%):', min_value=0.0, max_value=100.0, value=55.0)
    st.write('')
    vector_primera_bola = [bola1_7pinos, bola1_8pinos, bola1_9pinos, bola1_10pinos]

    #Probabilidades de la segunda bola. Genera el segundo vector de probabilidades
    st.subheader('📊Probabilidades de la Segunda bola:')
    st.markdown('🎳Con 7 pinos tirados en la primera bola')
    bola2_7_0pinos = st.number_input('Probabilidad de tirar 0 pinos (%):', min_value=0.0, max_value=100.0, value=2.0)
    bola2_7_1pinos = st.number_input('Probabilidad de tirar 1 pino (%):', min_value=0.0, max_value=100.0, value=10.0)
    bola2_7_2pinos = st.number_input('Probabilidad de tirar 2 pinos (%):', min_value=0.0, max_value=100.0, value=45.0)
    bola2_7_3pinos = st.number_input('Probabilidad de tirar 3 pinos (%):', min_value=0.0, max_value=100.0, value=43.0)

    st.markdown('🎳Con 8 pinos tirados en la primera bola')
    bola2_8_0pinos = st.number_input('Probabilidad de tirar 0 pinos (%):', min_value=0.0, max_value=100.0, value=4.0)
    bola2_8_1pinos = st.number_input('Probabilidad de tirar 1 pino (%):', min_value=0.0, max_value=100.0, value=20.0)
    bola2_8_2pinos = st.number_input('Probabilidad de tirar 2 pinos (%):', min_value=0.0, max_value=100.0, value=76.0)

    st.markdown('🎳Con 9 pinos tirados en la primera bola')
    bola2_9_0pinos = st.number_input('Probabilidad de tirar 0 pinos (%):', min_value=0.0, max_value=100.0, value=6.0)
    bola2_9_1pinos = st.number_input('Probabilidad de tirar 1 pino (%):', min_value=0.0, max_value=100.0, value=94.0)
    
    vector_segunda_bola_7 = [bola2_7_0pinos, bola2_7_1pinos, bola2_7_2pinos, bola2_7_3pinos] 
    vector_segunda_bola_8 = [bola2_8_0pinos, bola2_8_1pinos, bola2_8_2pinos]
    vector_segunda_bola_9 = [bola2_9_0pinos, bola2_9_1pinos]
    
    st.subheader('🎳Puntajes')
    puntaje_1 = st.number_input('Puntaje de tirar 10 pinos en el primer tiro', min_value=0, value=10)
    puntaje_2 = st.number_input('Puntaje de tirar 10 pinos entre los dos tiros', min_value=0, value=15)

    st.subheader('🎳Rondas')
    n_rondas = st.number_input('Rondas', min_value=0, value=10)
    
    puntaje_minimo_ronda = st.number_input('Puntaje mínimo por ronda', min_value=0, value=120)
    vector_segunda_bola = vector_segunda_bola_7 + vector_segunda_bola_8 + vector_segunda_bola_9

    sim_ok = st.button('✅Iniciar Simulación')
    if sim_ok:

        LoadSimulacion(vector_primera_bola, vector_segunda_bola, puntaje_1, puntaje_2, n_rondas, puntaje_minimo_ronda)


def LoadSimulacion(v1, v2, puntaje_1, puntaje_2, n_rondas, puntaje_minimo_ronda):
    st.write(
        'Un jugador de bowling tiene la siguiente distribución de probabilidad para el número de pinos tirados por la primera bola:')
    
    primera_bola = {'Número de pinos': [7, 8, 9, 10],
            'Probabilidad (%)': v1,
            'Probabilidad acumuladas': tablas.CrearIntervalos(v1)
            }
    df = pd.DataFrame(primera_bola, columns = ['Número de pinos','Probabilidad (%)','Probabilidad acumuladas'])
    st.write(df)

    acumulado_7 = tablas.CrearIntervalos(v2[0:4])
    acumulado_8 = tablas.CrearIntervalos(v2[4:7])
    acumulado_9 = tablas.CrearIntervalos(v2[7:9])
    st.write(acumulado_7)
    st.write(acumulado_8)
    st.write(acumulado_9)
    st.write('Las distribuciones de probabilidad para el número de pinos de la segunda bola son:')
    segunda_bola = {'Pinos de la primera bola': [7, 7, 7, 7, 8, 8, 8, 9, 9],
                    'Pinos de la segunda bola': [0, 1, 2, 3, 0, 1, 2, 0, 1],
                    'Probabilidad (%)': v2,
                    'Probabilidad acumuladas': acumulado_7 + acumulado_8 + acumulado_9
                    }
    df2 = pd.DataFrame(segunda_bola, columns = ['Pinos de la primera bola', 'Pinos de la segunda bola', 'Probabilidad (%)','Probabilidad acumuladas'])
    st.write(df2)

    









