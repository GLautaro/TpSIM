import streamlit as st
import pandas as pd

# The homepage is loaded using a combination of .write and .markdown.


def LoadPage():
    st.title('🔢Sistemas de Colas🔢')
    st.markdown('Simulación - Trabajo Práctico de Laboratorio 5')
    st.write('Se desarrollo esta aplicación que permite generar una simulación basada en un sistema multi-colas.')
    for i in range(2):
        st.write('')

    st.header('💬Sobre la Aplicación')
    st.write(
        'En el menú lateral usted podrá navegar las distintas funcionalidades de esta aplicación.')
    st.write(
        'Si selecciona "Simular" usted podra realizar la simulación y modificar los parametros de la misma')

    st.header('📝Ejercicio B: Inscripción a examenes.')
    st.write('Sea un lugar de inscripción a exámenes para alumnos de la UNVM, ' + 
        'existen 5 equipos para inscribirse y la inscripción demora de 5 a 8 minutos uniformemente distribuida.' +
        'Los alumnos llegan para inscribirse con una distribución exponencial negativa de media 2’. ' +
        'Cada 1 hora ± 3’ llega una persona de sistemas que hace mantenimiento preventivo a cada computadora, ' +
        'empezando por la primera que este libre (si hay varias, elige cualquiera), luego a otra y ' +
        'así sucesivamente, demorando un tiempo en cada equipo que responde a una normal media 3’ y ' +
        'desv. estándar 10”. Tiene prioridad sobre los alumnos.'  +
        'Si un alumno llega y hay más de 4 alumnos esperando, se va y regresa a la media hora: ')
    st.write('⭕ Determine el porcentaje de alumnos que se van para regresar más tarde.')
    st.write('⭕ Determine la capacidad de inscripción del sistema por hora en promedio (y por máquina).')
