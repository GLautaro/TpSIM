#Importacion del modulos propios
import Modulos.numbers as utils
import Modulos.GeneradoresAleatorios as generador

#Importacion de modulos de terceros
import streamlit as st

array = utils.generate_numbers(10)

def main():
    st.title('🔢Generador de números aleatorios🔢')

    array_length = st.number_input('Ingrese la cantidad de numeros que desea generar', min_value = 0, value=10, format='%d')
  
    
    opciones = ['Congruencial Lineal', 'Congruencial Multiplicativo', 'Función Nativa']

    opcion_seleccionada = st.selectbox(
    'Elegir Método:',
     list(range(len(opciones))), format_func= lambda x: opciones[x] )  
    gen_ok = st.button('Generar numeros')
    
    if gen_ok:  
        if opcion_seleccionada == 0:
            st.write(generador.ListaAleatoriaCongruencialLineal(array_length))
        elif opcion_seleccionada == 1:
            st.write(generador.ListaAleatoriaCongruencialMultiplicativo(array_length))
        elif opcion_seleccionada == 2:
            st.write(generador.ListaAleatoriaNativa(array_length))


if __name__ == "__main__":
    main()