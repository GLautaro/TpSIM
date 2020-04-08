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

def GeneradorHistograma(df_lista_numeros):
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=df_lista_numeros["Intervalo"],
        y=df_lista_numeros["Fo"],
        name='Obtenido',
        marker_color='#0E61FD',
        opacity=0.75
    ))

    fig.add_trace(go.Bar(
        x=df_lista_numeros["Intervalo"],
        y=df_lista_numeros["Fe"],
        name='Esperado',
        marker_color='#FD0E2F',
        opacity=0.55
    ))

    fig.update_layout(
        title_text='Histograma de frecuencias',  # title of plot
        xaxis_title_text='Intervalos',  # xaxis label
        yaxis_title_text='Cantidad',  # yaxis label
        bargap=0,  # gap between bars of adjacent location coordinates
        bargroupgap=0,  # gap between bars of the same location coordinates
        barmode='overlay'
    )

    return fig


def GenerarFrecuenciasEsperadas(cantidad_numeros, cantidad_intervalos):
    frecuencia_esperada = cantidad_numeros / cantidad_intervalos
    lista = [frecuencia_esperada] * cantidad_intervalos
    print(lista)
    return lista


if __name__ == "__main__":
    pass
