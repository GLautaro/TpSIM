# Importacion del modulos propios
import Modulos.GeneradoresAleatorios as generador
import Modulos.Constantes as constantes
import Modulos.GeneradorHistograma as histograma
import Modulos.PruebaChiCuadrado as chiCuadrado
from Modulos.Utils import GenerarExcel
import os

# Importacion de modulos de terceros
import streamlit as st

def LoadPage():
    st.title('🔢Generación de variables aleatorias')

    #Preparación del sidebar con todos sus inputs.
    array_length = st.sidebar.number_input(
        'Ingrese la cantidad de numeros que desea generar', min_value=0, value=10, format='%d')

    exportar_como_excel = st.sidebar.checkbox("Abrir como excel",value=True)

    opciones = ['Uniforme [a, b]',
                'Exponencial', 'Normal']
    
    st.sidebar.subheader('🔢Opciones del generador aleatorio:')

    opcion_seleccionada = st.sidebar.radio(
        'Elegir Distribución:',
        list(range(len(opciones))), format_func=lambda x: opciones[x])

    #Faltan poner mas parametros si hacen falta
    if opcion_seleccionada == 0:
        semilla = st.sidebar.number_input(
            'Semilla (X0):', min_value=0, value=0, format='%d')
    elif opcion_seleccionada == 1:
        var_lamdba = st.sidebar.number_input(
            'Lambda:', min_value=0, value=0)
    else:
        media = st.sidebar.number_input(
            'Media μ:', min_value=0, value=0)
        desviacion_est = st.sidebar.number_input(
            'Desviación estandar σ:', min_value=0, value=0)
    
    gen_ok = st.sidebar.button('Iniciar Simulación')
    if gen_ok:
            if opcion_seleccionada == 0:
                st.write('Generación aleatoria utilizando la distribución uniforme [a, b].')
                st.latex(r'''
                X = A + RND(B-A)
                ''')
            elif opcion_seleccionada == 1:
                st.write('Generación aleatoria utilizando la distribución exponencial.')
                st.latex(r'''
                X = \dfrac{-1}{\lambda} * \ln(1-RND)
                ''')
                st.latex(r'''
                siendo: \lambda = \dfrac {1} {\mu}
                ''')
            else:
                st.write('Generación aleatoria utilizando la distribución normal.')