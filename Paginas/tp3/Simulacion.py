# Importacion del modulos propios
import Modulos.GeneradoresAleatorios as generador
import Modulos.Constantes as constantes
import Modulos.GeneradorHistograma as histograma
import Modulos.PruebaChiCuadrado as chiCuadrado
from Modulos.Utils import GenerarExcel
import os

# Importacion de modulos de terceros
import streamlit as st
import pandas as pd
import numpy as np


def LoadPage():
    st.title('🔢Generación de variables aleatorias')

    # Preparación del sidebar con todos sus inputs.
    array_length = st.sidebar.number_input(
        'Ingrese la cantidad de numeros que desea generar', min_value=0, value=10, format='%d')

    exportar_como_excel = st.sidebar.checkbox("Abrir como excel", value=True)

    opciones = ['Uniforme [a, b]',
                'Exponencial', 'Normal']

    st.sidebar.subheader('🔢Opciones del generador aleatorio:')

    opcion_seleccionada = st.sidebar.radio(
        'Elegir Distribución:',
        list(range(len(opciones))), format_func=lambda x: opciones[x])

    # Faltan poner mas parametros si hacen falta
    if opcion_seleccionada == 0:
        semilla = st.sidebar.number_input(
            'Semilla (X0):', min_value=0, value=0, format='%d')
        extremo_a = st.sidebar.number_input(
            'Extremo a:', min_value=0, value=0, format='%d')
        extremo_b = st.sidebar.number_input(
            'Extremo b:', min_value=0, value=0, format='%d')
    elif opcion_seleccionada == 1:
        media = st.sidebar.number_input(
            'Media μ:', min_value=0.0, value=0.0)
    else:
        media = st.sidebar.number_input(
            'Media μ:', min_value=0.0, value=0.0)
        desviacion_est = st.sidebar.number_input(
            'Desviación estandar σ:', min_value=0.0, value=0.0)

    # Opciones del sidebar - Histograma y Chi-cuadrado
    st.sidebar.subheader('📊Opciones del histograma de frecuencias:')
    intervalos = st.sidebar.radio('Seleccione la cantidad de intervalos:',
                                  [5, 10, 15, 20])

    st.sidebar.subheader('📈Opciones de la prueba de Chi-Cuadrado:')
    nivel_significancia = st.sidebar.number_input(
        'Nivel de Significancia:', min_value=0.0, max_value=1.0)

    gen_ok = st.sidebar.button('Iniciar Simulación')
    if gen_ok:
        try:
            serie_numeros = []

            if opcion_seleccionada == 0:
                serie_numeros = generador.ListaAleatoriaNativa(
                    array_length, extremo_a, extremo_b, semilla)
                media = (extremo_b - extremo_a) / 2
                desviacion_est = np.std(serie_numeros, ddof=1)
                st.write(
                    'Generación aleatoria utilizando la distribución uniforme [a, b].')
                st.latex(r'''
                    X = A + RND(B-A)
                    ''')
            elif opcion_seleccionada == 1:
                serie_numeros = generador.distribucionExponencial(
                    array_length, media_exp)
                extremo_a, extremo_b = 0
                desviacion_est = np.std(serie_numeros, ddof=1)
                st.write('Generación aleatoria utilizando la distribución exponencial.')
                st.latex(r'''
                    X = \dfrac{-1}{\lambda} * \ln(1-RND)
                    ''')
                st.latex(r'''
                    siendo: \lambda = \dfrac {1} {\mu}
                    ''')
            else:
                st.write('Generación aleatoria utilizando la distribución normal.')
                serie_numeros = generador.distribucionNormal(array_length, media, desviacion_est)
                extremo_a, extremo_b = 0

            df_numeros = pd.DataFrame(serie_numeros)

            st.write(df_numeros)

            resultado, valor_critico, df_tabla, grados_libertad = chiCuadrado.PruebaChiCuadrado(
                serie_numeros, intervalos, nivel_significancia, opcion_seleccionada, media, desviacion_est, extremo_a, extremo_b)

            st.write(histograma.GeneradorHistograma(df_tabla))

            st.subheader("📊Prueba Chi Cuadrado")
                
            tabla_chi = go.Figure(data=[go.Table(
                header=dict(values=["Intervalo", "Fo", "Fe", "C", "C(ac)"],
                fill_color='paleturquoise',
                align='center'),
                cells=dict(values=[df_tabla.Intervalo, df_tabla.Fo, df_tabla.Fe, df_tabla.C, df_tabla["C(ac)"]],
                fill_color='lavender',
                align='center'))
            ])
            st.write(tabla_chi)

            if resultado == constantes.ResultadosChi2.H0_NO_RECHAZABLE:
                st.write("Para un nivel de significancia de " + str(nivel_significancia), "y un valor crítico de: " + str(valor_critico), ". La prueba de Chi Cuadrado considera la Hipotesis Nula como No Rechazable")
            else:
                st.write("Para un nivel de significancia de " + str(nivel_significancia), "y un valor crítico de: " + str(valor_critico), " .La prueba de Chi Cuadrado considera la Hipotesis Nula como Rechazada")


            if exportar_como_excel:
                nombre_archivo = "tabla_numeros.xlsx"
                GenerarExcel({
                    "Lista_Valores_Aleatorios": df_numeros,
                    "Tabla_prueba_Chi2": df_tabla[["Intervalo","Fo","Fe","C","C(ac)"]]
                },
                    nombre_archivo)
                os.startfile(nombre_archivo)
  
        except ZeroDivisionError as err:
            st.error(
                'Ups! Ocurrió un error, revise los parametros ingresados. Error:' + str(err))
        except Exception as err:
            st.error("Ups! Ocurrió un error. Error: " + str(err))
