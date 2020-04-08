# Importacion del modulos propios
import Modulos.GeneradoresAleatorios as generador
import Modulos.Constantes as constantes
import Modulos.GeneradorHistograma as histograma
import Modulos.PruebaChiCuadrado as chiCuadrado

# Importacion de modulos de terceros
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def LoadPage():
    st.title('🔢Numeros Aleatorios')
    array_length = st.sidebar.number_input(
        'Ingrese la cantidad de numeros que desea generar', min_value=0, value=10, format='%d')

    opciones = ['Congruencial Lineal',
                'Congruencial Multiplicativo', 'Función Nativa']

    st.sidebar.subheader('🔢Opciones del generador aleatorio:')
    opcion_seleccionada = st.sidebar.radio(
        'Elegir Método:',
        list(range(len(opciones))), format_func=lambda x: opciones[x])

    if opcion_seleccionada != 2:
        semilla = st.sidebar.number_input(
            'Semilla (X0):', min_value=0, value=0, format='%d')
        entero_k = st.sidebar.number_input(
            'Entero (k) para obtener la constante multiplicativa:', min_value=0, value=0, format='%d')
        entero_g = st.sidebar.number_input(
            'Entero (g) para obtener el módulo:', min_value=0, value=0, format='%d')
        constante_aditiva = 0
        if opcion_seleccionada == 0:
            constante_aditiva = st.sidebar.number_input(
                'Constante Aditiva (c):', min_value=0, value=0, format='%d')
    else:
        semilla = st.sidebar.number_input(
            'Semilla (X0):', min_value=-1, value=0, format='%d')
        constante_aditiva, entero_k, entero_g, = 0, 0, 0

    st.sidebar.subheader('📊Opciones del histograma de frecuencias:')
    intervalos = st.sidebar.radio('Seleccione la cantidad de intervalos:',
                                   [5, 10, 15, 20])

    st.sidebar.subheader('📈Opciones de la prueba de Chi-Cuadrado:')
    nivel_significancia = st.sidebar.number_input(
        'Nivel de Significancia:', min_value=0.0, max_value=1.0)

    gen_ok = st.sidebar.button('Iniciar Simulación')
    if gen_ok:
        try:
            lista_numeros = {"Numero generado": generador.ListaNumerosAleatorios(
                opcion_seleccionada, array_length, semilla, entero_k, entero_g, constante_aditiva)}

            if opcion_seleccionada == 0:
                st.write('Generación aleatoria utilizando el metodo congruencial lineal.')
                st.latex(r'''
                X_{i+1} = (a.X_i + c) \mod(m)
                ''')
                st.latex(r'''
                rnd_i = \dfrac {X_i} {m-1}
                ''')
            elif opcion_seleccionada == 1:
                st.write('Generación aleatoria utilizando el metodo congruencial multiplicativo.')
                st.latex(r'''
                X_{i+1} = (a.X_i) \mod(m)
                ''')
                st.latex(r'''
                rnd_i = \dfrac {X_i} {m-1}
                ''')
            else:
                st.write('Generación aleatoria utilizando el metodo nativo de Python Random.')

            df_numeros = pd.DataFrame(lista_numeros)

            st.write('Listado de números generados:')
            #st.write(df_numeros)
            tabla_valores = go.Figure(data=[go.Table(
                header=dict(values= ["Iteracion"] + list(df_numeros.columns),
                fill_color='paleturquoise',
                align='center'),
                cells=dict(values=[df_numeros.index, df_numeros["Numero generado"]],
                fill_color='lavender',
                align='center'))
            ])

            st.write(tabla_valores)




            resultado, valor_critico, df_tabla, grados_libertad = chiCuadrado.PruebaChiCuadrado(list(lista_numeros["Numero generado"]), intervalos, nivel_significancia)

            st.write(histograma.GeneradorHistograma(df_tabla))
            
            st.subheader("📊Prueba Chi Cuadrado")
            
            tabla_chi = go.Figure(data=[go.Table(
                header=dict(values=["Intervalo", "Fo", "Fe", "C", "C(ac)"],
                fill_color='paleturquoise',
                align='center'),
                cells=dict(values=[df_tabla.Intervalo, df_tabla.Fo, df_tabla.Fe, df_tabla.C, df_tabla["C(ac)"]],
                fill_color='lavender',
                align='center'))
            ])
            st.write(tabla_chi)

            if resultado == constantes.ResultadosChi2.H0_NO_RECHAZABLE:
                st.write("Para un nivel de significancia de " + str(nivel_significancia), "y un valor crítico de: " + str(valor_critico), ". La prueba de Chi Cuadrado considera la Hipotesis Nula como No Rechazable")
            else:
                st.write("Para un nivel de significancia de " + str(nivel_significancia), "y un valor crítico de: " + str(valor_critico), " .La prueba de Chi Cuadrado considera la Hipotesis Nula como Rechazada")


        except ZeroDivisionError as err:
            st.error(
                'Ups! Ocurrió un error, revise los parametros ingresados. Error:' + str(err))
        except Exception as err:
            st.error("Ups! Ocurrió un error. Error: " + str(err))



