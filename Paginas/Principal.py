import streamlit as st

## The homepage is loaded using a combination of .write and .markdown.

def LoadPage():
    st.title('🔢Generador de números aleatorios🔢')
    st.markdown('Simulación - Trabajo Práctico de Laboratorio 1')
    st.write('Se desarrollo esta aplicación que permite generar series de numeros aleatorios, visualizar '
            'histogramas de frecuencias y realizar la prueba de Chi-Cuadrado.')
    for i in range(3):
        st.write('')

    st.header('💬Sobre la Aplicación')
    st.write('En el menú lateral usted podrá navegar las distintas funcionalidades de esta aplicación.')
    st.write('Estas son las páginas disponibles en la aplicación:')
    st.subheader('🔢Numeros Aleatorios.')
    st.markdown('Permite generar una serie de numeros aleatorios utilizando ' 
                'los metodos congruenciales mixto y multipticativo.')
    st.subheader('📊Prueba de Chi-Cuadrado.')   
    st.markdown('Permite generar una serie de numeros aleatorios y a esta se le aplica el test ' 
                'de Chi-Cuadrado y muestra el histograma de frecuencias.')

