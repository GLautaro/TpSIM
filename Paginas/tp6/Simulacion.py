import streamlit as st
import Soporte.ControladorSimuladorColas as csc
import os
import Modulos.Utils as u

def LoadPage():
    st.title('Inscripcion a examenes')
    st.markdown('Ingrese los parametros solicitados y luego presione "Iniciar Simulacion".')

    #Parametros de la simulacion y visualizacion
    st.header('🔧Parametros de simulación.')
    tiempo = st.number_input('Tiempo a simular (minutos)', min_value=0.0, value=1000.0)
    cant_iteraciones = st.number_input('Cantidad de iteraciones a mostrar', min_value=0, value=500, format='%d')
    min_iteraciones = st.number_input('Minutos desde la cual se muestran las iteraciones', min_value=0.0, value=0.0)

    #Parametros de la demora de inscripcion (distribucion uniforme A-B)
    st.header('⏲Parametros de la demora de inscripcion.')
    st.markdown('Se solicitan los parametros correspondientes a una distribucion uniforme (A-B)')
    a_uniforme_ins = st.number_input('A', value=5, format='%d')
    b_uniforme_ins = st.number_input('B', value=8, format='%d')

    #Parametros de llegada de alumnos (distribucion exponencial negativa)
    st.header('🏃Parametros de llegada de alumnos.')
    st.markdown('Se solicitan los parametros correspondientes a una distribucion exponencial negativa')
    exp_neg_media = st.number_input('Media μ:', min_value=0.0, value=5.0)

    #Parametros de llegada de mantenimiento (distribucion uniforme A-B)
    st.header('👷Parametros de llegada de manteminiento.')
    st.markdown('Se solicitan los parametros correspondientes a una distribucion uniforme (A-B)')
    a_uniforme_mant = st.number_input('A:', value=15, format='%d')
    b_uniforme_mant = st.number_input('B:', value=30, format='%d')

    #Parametros de demora de mantenimiento (distribucion normal)
    st.header('📓💻Parametros de cantidad de archivos.')
    st.markdown('Se solicitan los parametros correspondientes a la cantidad de archivos en las computadoras.')
    prob_1000 = st.number_input('Probabilidad de que sean 1000 archivos(%):', min_value=0.0, max_value=100.0, value=25.0)
    prob_1500 = st.number_input('Probabilidad de que sean 1500 archivos(%):', min_value=0.0, max_value=100.0, value=50.0)
    prob_2000 = st.number_input('Probabilidad de que sean 2000 archivos(%):', min_value=0.0, max_value=100.0, value=25.0)

    #-----------------------
    #Fin seccion parametros
    #-----------------------

    simulacion_ok = st.button('Iniciar simulación')
    if simulacion_ok:
        # Falta modulo con modificacion de ec. diferencial
        pass