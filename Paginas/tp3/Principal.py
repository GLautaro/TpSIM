import streamlit as st

## The homepage is loaded using a combination of .write and .markdown.

def LoadPage():
    st.title('🔢Simulación con distribuciones probabilisticas continuas.🔢')
    st.markdown('Simulación - Trabajo Práctico de Laboratorio 2')
    st.write('Se desarrollo esta aplicación que permite generar series de numeros aleatorios utilizando distintas distribuciones, visualizar '
            'histogramas de frecuencias y realizar la prueba de Chi-Cuadrado.')
    for i in range(2):
        st.write('')

    st.header('💬Sobre la Aplicación')
    st.write('En el menú lateral usted podrá navegar las distintas funcionalidades de esta aplicación.')
    st.write('Si selecciona "Simular" usted podra realizar las siguientes funcionalidades:')
    st.subheader('🔢Generador aleatorio.')
    st.markdown('Permite generar una serie de numeros aleatorios utilizando ' 
                'las distribuciones uniforme [a, b], exponencial y normal.')
    st.subheader('📊Prueba de Chi-Cuadrado.')   
    st.markdown('Permite aplicar el test de Chi-Cuadrado ' 
                'a la serie de numeros y muestra el histograma de frecuencias.')