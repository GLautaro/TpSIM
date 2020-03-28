#Importacion del modulos propios
import Modulos.numbers as utils
import Modulos.GeneradoresAleatorios as generador

#Importacion de modulos de terceros
import streamlit as st

array = utils.generate_numbers(10)

def main():
    st.title('🔢Generador de números aleatorios🔢')

    array_length = st.number_input('Ingrese la cantidad de numeros que desea generar', min_value = 0, value=10, format='%d')
  
    
    options = ['Congruencial Lineal', 'Congruencial Multiplicativa', 'Función Nativa']

    option_selected = st.selectbox(
    'Elegir Método:',
     list(range(len(options))), format_func= lambda x: options[x] )  
    gen_ok = st.button('Generar numeros')
    
    if gen_ok:  
        if option_selected == 0:
            st.write(generador.ListaAleatoriaCongruenciaLineal(array_length))
        elif option_selected == 1:
            st.write(generador.ListaAleatoriaCongruenciaMultiplicativa(array_length))
        elif option_selected == 2:
            st.write(generador.ListaAleatoriaNativa(array_length))


if __name__ == "__main__":
    main()