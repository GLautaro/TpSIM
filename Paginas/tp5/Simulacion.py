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
    cant_iteraciones = st.number_input('Cantidad de iteraciones a mostrar', min_value=0.0, value=500.0)
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
    st.header('👷🕒Parametros de demora de manteminiento.')
    st.markdown('Se solicitan los parametros correspondientes a una distribucion normal')
    media_demora = st.number_input('Media μ', min_value=0.0, value=10.0)
    desviacion_est_demora = st.number_input('Desviación estandar σ', min_value=0.0, value=3.0)

    #-----------------------
    #Fin seccion parametros
    #-----------------------

    simulacion_ok = st.button('Iniciar simulación')
    if simulacion_ok:
        controlador = csc.Controlador(tiempo, 0, a_uniforme_ins, b_uniforme_ins, exp_neg_media, a_uniforme_mant, b_uniforme_mant, media_demora, desviacion_est_demora, min_iteraciones, cant_iteraciones)
        os.system("taskkill /F /IM excel.exe")
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
        df, cant_ins_m1, cant_ins_m2, cant_ins_m3, cant_ins_m4, cant_ins_m5, cant_al_llegaron, cant_al_retiran = controlador.simular()
        nombre = "tp5.xlsx"
        u.GenerarExcel({"Simulacion": df}, nombre)
        os.startfile(nombre)
        st.title("Capacidad de inscripción")
        st.header("💻Máquina 1")
        st.write("Cantidad de inscripciones: ", cant_ins_m1)
        st.write("Cantidad de inscripciones por hora: ", u.Truncate(cant_ins_m1/(tiempo/60), 2))
        st.header("💻Máquina 2")
        st.write("Cantidad de inscripciones: ", cant_ins_m2)
        st.write("Cantidad de inscripciones por hora: ", u.Truncate(cant_ins_m2/(tiempo/60), 2))
        st.header("💻Máquina 3")
        st.write("Cantidad de inscripciones: ", cant_ins_m3)
        st.write("Cantidad de inscripciones por hora: ", u.Truncate(cant_ins_m3/(tiempo/60), 2))
        st.header("💻Máquina 4")
        st.write("Cantidad de inscripciones: ", cant_ins_m4)
        st.write("Cantidad de inscripciones por hora: ", u.Truncate(cant_ins_m4/(tiempo/60), 2))
        st.header("💻Máquina 5")
        st.write("Cantidad de inscripciones: ", cant_ins_m5)
        st.write("Cantidad de inscripciones por hora: ", u.Truncate(cant_ins_m5/(tiempo/60), 2))
        st.title("Porcentaje de alumnos que se retiraron ")
        st.write("🏃Cantidad de alumnos que llegaron: ", cant_al_llegaron)
        st.write("🚫📝Cantidad de alumnos que se retiraron: ", cant_al_retiran)
        st.write("Porcentaje: ", u.Truncate((cant_al_retiran/cant_al_llegaron)*100, 2), "%")

