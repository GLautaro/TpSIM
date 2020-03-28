#Importacion del modulos propios
import Modulos.GeneradoresAleatorios as generador
import Modulos.Constantes as constantes
import Modulos.GeneradorHistograma as histograma

#Importacion de modulos de terceros
import streamlit as st

def main():
    st.title('🔢Generador de números aleatorios🔢')

    array_length = st.number_input('Ingrese la cantidad de numeros que desea generar', min_value = 0, value=10, format='%d')
  
    opciones = ['Congruencial Lineal', 'Congruencial Multiplicativo', 'Función Nativa']

    opcion_seleccionada = st.selectbox(
    'Elegir Método:',
     list(range(len(opciones))), format_func= lambda x: opciones[x] )  
    gen_ok = st.button('Generar numeros')
    
    if gen_ok:
        lista_numeros = generador.ListaNumerosAleatorios(array_length, opcion_seleccionada)

        st.write(lista_numeros)

        st.subheader('Histograma de frecuencias')

        st.write(histograma.GeneradorHistograma(lista_numeros, 10))




if __name__ == "__main__":
    main()