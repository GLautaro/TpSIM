# Importacion de paginas
import Paginas.tp1.Principal as principal
import Paginas.tp1.NumerosAleatorios as numeros_aleatorios

# Importacion de modulos de terceros
import streamlit as st


def CreateLayout():
    st.sidebar.title("Menú")
    app_mode = st.sidebar.selectbox("Seleccione una página:",
                                    ["Introducción", "Principal"])
    
    if app_mode == 'Introducción':
        principal.LoadPage()
    else:
        numeros_aleatorios.LoadPage()


if __name__ == "__main__":
    CreateLayout()
