#Importacion de paginas
import Paginas.Principal as principal
import Paginas.NumerosAleatorios as numeros_aleatorios
import Paginas.ChiCuadrado as chi_cuadrado

#Importacion de modulos de terceros
import streamlit as st

def CreateLayout():
    st.sidebar.title("Menú")
    app_mode = st.sidebar.selectbox("Seleccione una página:", 
    ["Principal", "Numeros Aleatorios", "Prueba de Chi-Cuadrado"])

    if app_mode == 'Principal':
        principal.LoadPage()
    elif app_mode == "Numeros Aleatorios":
        numeros_aleatorios.LoadPage()
    elif app_mode == "Prueba de Chi-Cuadrado":
        chi_cuadrado.LoadPage()

if __name__ == "__main__":
    CreateLayout()