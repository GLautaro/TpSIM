# Importacion del modulos propios
import Modulos.GeneradoresAleatorios as generador
import Modulos.Constantes as constantes
import Modulos.GeneradorHistograma as histograma
import Modulos.PruebaChiCuadrado as chiCuadrado

# Importacion de modulos de terceros
import streamlit as st
import pandas as pd


def LoadPage():
    st.title('🔢Numeros Aleatorios')
    array_length = st.sidebar.number_input(
        'Ingrese la cantidad de numeros que desea generar', min_value=0, value=10, format='%d')

    opciones = ['Congruencial Lineal',
                'Congruencial Multiplicativo', 'Función Nativa']

    st.sidebar.subheader('🔢Opciones del generador aleatorio:')
    opcion_seleccionada = st.sidebar.radio(
        'Elegir Método:',
        list(range(len(opciones))), format_func=lambda x: opciones[x])

    semilla = st.sidebar.number_input(
            'Semilla (X0):', min_value=0, value=0, format='%d')
            
    if opcion_seleccionada != 2:
        
        # TODO: CAMBIAR POR K
        constante_multiplicativa = st.sidebar.number_input(
            'Constante multiplicativa (a):', min_value=0, value=0, format='%d')
        # TODO: CAMBIAR POR G
        modulo = st.sidebar.number_input(
            'Módulo (m):', min_value=0, value=0, format='%d')
        constante_aditiva = 0
        if opcion_seleccionada == 0:
            constante_aditiva = st.sidebar.number_input(
                'Constante Aditiva (c):', min_value=0, value=0, format='%d')
    else:
        semilla, constante_aditiva, constante_multiplicativa, modulo, = 0, 0, 0, 0

    st.sidebar.subheader('📊Opciones del histograma de frecuencias:')
    intervalos = st.sidebar.slider('Seleccione la cantidad de intervalos:',
                                   min_value=5, value=5, max_value=20, step=5)

    st.sidebar.subheader('📈Opciones de la prueba de Chi-Cuadrado:')
    nivel_significancia = st.sidebar.number_input(
        'Nivel de Significancia:', min_value=0.0, max_value=100.0)

    gen_ok = st.sidebar.button('Iniciar Simulación')
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
