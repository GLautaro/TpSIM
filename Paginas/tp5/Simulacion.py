import streamlit as st

def LoadPage():
    st.title('Inscripcion a examenes')
    st.markdown('Ingrese los parametros solicitados y luego presione "Iniciar Simulacion".')

    #Parametros de la simulacion y visualizacion
    st.header('🔧Parametros de simulación.')
    tiempo = st.number_input('Tiempo a simular (minutos)', min_value=0.0, value=10.0)
    iteraciones = st.number_input('Cantidad de iteraciones', min_value=0.0, max_value=1000000.0, value=20.0)
    cant_iteraciones = st.number_input('Cantidad de iteraciones a mostrar', min_value=0.0, value=5.0)
    min_iteraciones = st.number_input('Minutos desde la cual se muestran las iteraciones', min_value=0.0, value=1.0)

    #Parametros de la demora de inscripcion (distribucion uniforme A-B)
    st.header('⏲Parametros de la demora de inscripcion.')
    st.markdown('Se solicitan los parametros correspondientes a una distribucion uniforme (A-B)')
    a_uniforme = st.number_input('A', value=5, format='%d')
    b_uniforme = st.number_input('B', value=8, format='%d')

    #Parametros de llegada de alumnos (distribucion exponencial negativa)
    st.header('🏃Parametros de llegada de alumnos.')
    st.markdown('Se solicitan los parametros correspondientes a una distribucion exponencial negativa')
    exp_neg_media = st.number_input('Media μ:', min_value=0.0, value=1.0)

    #Parametros de llegada de mantenimiento (distribucion normal)
    st.header('👷Parametros de llegada de manteminiento.')
    st.markdown('Se solicitan los parametros correspondientes a una distribucion normal')
    media_manten = st.number_input('Media μ:', min_value=0.0, value=0.0)
    desviacion_est_manten = st.number_input('Desviación estandar σ:', min_value=0.0, value=1.0)

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
        Simular()


def Simular():
    ## TODO: Agregar funciones de simulación.

