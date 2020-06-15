import streamlit as st
import Soporte.ControladorSimuladorColas as csc
import os
import Modulos.Utils as u

def LoadPage():
    st.title('Inscripcion a examenes')
    st.markdown('Ingrese los parametros solicitados y luego presione "Iniciar Simulacion".')

    #Parametros de la simulacion y visualizacion
    st.header('🔧Parametros de simulación.')
    tiempo = st.number_input('Tiempo a simular (minutos)', min_value=0.0, value=10.0)
    cant_iteraciones = st.number_input('Cantidad de iteraciones a mostrar', min_value=0.0, value=5.0)
    min_iteraciones = st.number_input('Minutos desde la cual se muestran las iteraciones', min_value=0.0, value=1.0)

    #Parametros de la demora de inscripcion (distribucion uniforme A-B)
    st.header('⏲Parametros de la demora de inscripcion.')
    st.markdown('Se solicitan los parametros correspondientes a una distribucion uniforme (A-B)')
    a_uniforme_ins = st.number_input('A', value=5, format='%d')
    b_uniforme_ins = st.number_input('B', value=8, format='%d')

    #Parametros de llegada de alumnos (distribucion exponencial negativa)
    st.header('🏃Parametros de llegada de alumnos.')
    st.markdown('Se solicitan los parametros correspondientes a una distribucion exponencial negativa')
    exp_neg_media = st.number_input('Media μ:', min_value=0.0, value=1.0)

    #Parametros de llegada de mantenimiento (distribucion uniforme A-B)
    st.header('👷Parametros de llegada de manteminiento.')
    st.markdown('Se solicitan los parametros correspondientes a una distribucion uniforme (A-B)')
    a_uniforme_mant = st.number_input('A:', value=5, format='%d')
    b_uniforme_mant = st.number_input('B:', value=8, format='%d')

    #Parametros de demora de mantenimiento (distribucion normal)
    st.header('👷🕒Parametros de demora de manteminiento.')
    st.markdown('Se solicitan los parametros correspondientes a una distribucion normal')
    media_demora = st.number_input('Media μ', min_value=0.0, value=0.0)
    desviacion_est_demora = st.number_input('Desviación estandar σ', min_value=0.0, value=1.0)

    #-----------------------
    #Fin seccion parametros
    #-----------------------

    simulacion_ok = st.button('Iniciar simulación')
    if simulacion_ok:
        controlador = csc.Controlador(tiempo, 0, a_uniforme_ins, b_uniforme_ins, exp_neg_media, a_uniforme_mant, b_uniforme_mant, media_demora, desviacion_est_demora, min_iteraciones, cant_iteraciones)
        #1 x = Tiempo a simular
        #2 reloj
        #3 a_insc
        #4 b_insc 
        #5 media_llegada_al
        #6 a_mant 
        #7 b_mant 
        #8 media_demora_mant 
        #9 desv_demora_mant
        #10 mostrar_desde_minuto
        #11 mostrar_cantidad_iteraciones
        df, acum_alumnos_llegaron, acum_alumnos_retiran = controlador.simular()
        nombre = "tp5.xlsx"
        u.GenerarExcel({"Simulacion": df}, nombre)
        os.startfile(nombre)
