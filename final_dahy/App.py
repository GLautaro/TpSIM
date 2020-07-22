import streamlit as st
import os
from Simulacion import Controlador
import Utils as u

st.title('🔢Sistemas de Colas🔢')
st.markdown('Ingrese los parametros solicitados y luego presione "Iniciar Simulacion".')

#Parametros de la simulacion y visualizacion}

st.header('🔧Parametros de simulación.')
tiempo = st.number_input('Tiempo a simular: ', min_value=0.0, value=100.0)
cant_iteraciones = st.number_input('Cantidad de iteraciones a mostrar: ', min_value=0, value=500)
mostrar_desde = st.number_input('Minutos desde la cual se muestran las iteraciones: ', min_value=0, value=500)

st.header('⏲Parametros de los eventos.')
media_llegada = st.number_input('Media llegada clientes (Poisson):', value=3, format='%d')
media_fin = st.number_input('Media fin de atención (Exp- Neg.):', value=5, format='%d')

simulacion_ok = st.button('Iniciar simulación')

if simulacion_ok:
    controlador = Controlador(cant_iteraciones, tiempo, mostrar_desde, media_llegada, media_fin)
    os.system("taskkill /F /IM excel.exe")
    df = controlador.simular()
    nombre = "examenFinal.xlsx"
    u.GenerarExcel({"Simulacion": df}, nombre)
    os.startfile(nombre)