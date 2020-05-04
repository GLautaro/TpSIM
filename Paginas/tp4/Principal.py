import streamlit as st
import pandas as pd

# The homepage is loaded using a combination of .write and .markdown.


def LoadPage():
    st.title('🔢Simulación de Montecarlo🔢')
    st.markdown('Simulación - Trabajo Práctico de Laboratorio 3')
    st.write('Se desarrollo esta aplicación que permite generar una simulación de un sistema utilizando la simulación de Montecarlo.')
    for i in range(2):
        st.write('')

    st.header('💬Sobre la Aplicación')
    st.write(
        'En el menú lateral usted podrá navegar las distintas funcionalidades de esta aplicación.')
    st.write(
        'Si selecciona "Simular" usted podra realizar la simulación y modificar los parametros de la misma')

    st.header('💬Ejercicio 24: Bowling.')
    st.write(
        'Un jugador de bowling tiene la siguiente distribución de probabilidad para el número de pinos tirados por la primera bola:')
    
    primera_bola = {'Número de pinos': [7, 8, 9, 10],
            'Probabilidad (%)': [12, 15, 18, 55]}

    df = pd.DataFrame(primera_bola, columns = ['Número de pinos','Probabilidad (%)'])
    st.write(df)

    st.write('Las distribuciones de probabilidad para el número de pinos de la segunda bola son:')

    segunda_bola = {'Pinos de la primera bola': [7, 7, 7, 7, 8, 8, 8, 9, 9],
                    'Pinos de la segunda bola': [0, 1, 2, 3, 0, 1, 2, 0, 1],
                    'Probabilidad (%)': [2, 10, 45, 43, 4, 20, 76, 6, 94]}

    df2 = pd.DataFrame(segunda_bola, columns = ['Pinos de la primera bola', 'Pinos de la segunda bola', 'Probabilidad (%)'])
    st.write(df2)

    st.write('Si tirar 10 pinos con el primer tiro significa 20 puntos, tirar 10 pinos con los dos tiros 15 puntos y en el resto de los casos se cuenta como puntaje el total de pinos tirados. Determinar la probabilidad de que en 10 rondas el jugador obtenga más de 120 puntos.')


