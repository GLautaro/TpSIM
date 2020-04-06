import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

'''
La funcion genera una Figure de Plotly (grafico) de Histograma
Parametros: 
lista_numeros (List): array con numeros aleatorios generados previamente
cantidad_intervalos: cantidad de intervalos que se mostraran en el histograma
Retorna: histograma: grafico de la libreria plotly
'''

def GeneradorHistograma(df_lista_numeros, cantidad_intervalos):

    frecuencia_esp = GenerarFrecuenciasEsperadas(
        df_lista_numeros.size, cantidad_intervalos)

    fig = go.Figure()

    fig.add_trace(go.Histogram(
        x=df_lista_numeros['Número generado'],
        name='Obtenido',
        marker_color='#330C73',
        opacity=0.75,
        xbins=dict(
            start=0.0,
            end=1.0,
            size=1 / cantidad_intervalos
        )
    ))

    """ 
    fig.add_trace(go.Histogram(
        x = df_lista_numeros['Número generado'],
        y = frecuencia_esp,
        name = 'Esperado',
        marker_color='#EB89B5',
        opacity=0.75
    )) """

    fig.update_layout(
        title_text='Histograma de frecuencias',  # title of plot
        xaxis_title_text='Intervalos',  # xaxis label
        yaxis_title_text='Cantidad',  # yaxis label
        bargap=0.2,  # gap between bars of adjacent location coordinates
        bargroupgap=0.1  # gap between bars of the same location coordinates
    )

    return fig


def GenerarFrecuenciasEsperadas(tamaño_muestra, cantidad_intervalos):
    frecuencia_esperada = tamaño_muestra / cantidad_intervalos
    lista = [frecuencia_esperada] * cantidad_intervalos
    return lista


if __name__ == "__main__":
    pass
