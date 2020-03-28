#Importacion del modulos propios
import Modulos.numbers as utils
import Modulos.GeneradoresAleatorios as generador

#Importacion de modulos de terceros
import streamlit as st

array = utils.generate_numbers(10)

def main():
    st.title('🔢Generador de números aleatorios🔢')

    array_length = st.number_input('Ingrese la cantidad de numeros que desea generar', min_value = 0, value=10, format='%d')
    gen_ok = st.button('Generar numeros')
    if gen_ok:
        st.write(utils.generate_numbers(array_length))

if __name__ == "__main__":
    main()