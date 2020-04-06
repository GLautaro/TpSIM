# Importacion del modulos propios
import Modulos.GeneradoresAleatorios as generador
import Modulos.Constantes as constantes
import Modulos.GeneradorHistograma as histograma

# Importacion de modulos de terceros
import streamlit as st
import pandas as pd


def LoadPage():
    st.title('🔢Numeros Aleatorios')
    array_length = st.number_input(
        'Ingrese la cantidad de numeros que desea generar', min_value=0, value=10, format='%d')

    opciones = ['Congruencial Lineal',
                'Congruencial Multiplicativo', 'Función Nativa']

    st.subheader('🔢Opciones del generador aleatorio:')
    opcion_seleccionada = st.radio(
        'Elegir Método:',
        list(range(len(opciones))), format_func=lambda x: opciones[x])

    if opcion_seleccionada != 2:
        semilla = st.number_input(
            'Semilla (X0):', min_value=0, value=0, format='%d')
        constante_multiplicativa = st.number_input(
            'Constante multiplicativa (a):', min_value=0, value=0, format='%d')
        modulo = st.number_input(
            'Módulo (m):', min_value=0, value=0, format='%d')
        constante_aditiva = 0
        if opcion_seleccionada == 0:
            constante_aditiva = st.number_input(
                'Constante Aditiva (c):', min_value=0, value=0, format='%d')
    else:
        semilla, constante_aditiva, constante_multiplicativa, modulo, = 0, 0, 0, 0

    st.subheader('📊Opciones del histograma de frecuencias:')
    intervalos = st.slider('Seleccione la cantidad de intervalos:',
                           min_value=5, value=5, max_value=20, step=5)

    gen_ok = st.button('Iniciar Simulación')
    if gen_ok:
        try:
            lista_numeros = generador.ListaNumerosAleatorios(
                opcion_seleccionada, array_length, semilla, constante_multiplicativa, modulo, constante_aditiva)
            df_numeros = pd.DataFrame(
                lista_numeros, columns=['Número generado'])

            st.subheader('Listado de números generados:')
            st.write(df_numeros)

            st.write(histograma.GeneradorHistograma(df_numeros, intervalos))

        except ZeroDivisionError as err:
            st.error(
                'Ups! Ocurrió un error, revise los parametros ingresados. Error:' + str(err))
        except:
            st.error("Ups! Ocurrió un error. Error:" + str(err))
