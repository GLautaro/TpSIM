#Importacion del modulos propios
import Modulos.GeneradoresAleatorios as generador
import Modulos.Constantes as constantes
import Modulos.GeneradorHistograma as histograma

#Importacion de modulos de terceros
import streamlit as st

def LoadPage():
    st.title('🔢Numeros Aleatorios')
    array_length = st.number_input('Ingrese la cantidad de numeros que desea generar', min_value = 0, value=10, format='%d')
  
    opciones = ['Congruencial Lineal', 'Congruencial Multiplicativo', 'Función Nativa']

    opcion_seleccionada = st.radio(
    'Elegir Método:',
     list(range(len(opciones))), format_func= lambda x: opciones[x])

    if opcion_seleccionada != 2:
        semilla = st.number_input('Semilla:', min_value = 0,value=0, format='%d')
        constante_multiplicativa = st.number_input('Constante multiplicativa:', min_value = 0,value=0, format='%d')
        modulo = st.number_input('Módulo:', min_value = 0, value= 0, format='%d')
        constante_aditiva = 0
        if opcion_seleccionada == 0:
            constante_aditiva = st.number_input('Constante Aditiva:', min_value = 0,value=0, format='%d')
    else:
        semilla, constante_aditiva, constante_multiplicativa, modulo, = 0, 0, 0, 0
    gen_ok = st.button('Generar numeros')
    if gen_ok:
        try:
            lista_numeros = generador.ListaNumerosAleatorios(opcion_seleccionada, array_length, semilla, constante_multiplicativa, modulo, constante_aditiva)

            st.write(lista_numeros)

            st.subheader('Histograma de frecuencias')

            st.write(histograma.GeneradorHistograma(lista_numeros, 10))
        
        except ZeroDivisionError as err:
            st.error('Ups! Ocurrió un error, revise los parametros ingresados. Error:' + str(err))
        except:
            st.error("Ups! Ocurrió un error. Error:"+ str(err) )
     
