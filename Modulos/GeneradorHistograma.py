import pandas as pd
import plotly.express as px

'''
La funcion genera una Figure de Plotly (grafico) de Histograma
Parametros: 
lista_numeros (List): array con numeros aleatorios generados previamente
cantidad_intervalos: cantidad de intervalos que se mostraran en el histograma
Retorna: histograma: grafico de la libreria plotly
'''

def GeneradorHistograma(lista_numeros, cantidad_intervalos):   
    df = pd.DataFrame(lista_numeros, columns=['Numeros generados'])
    figure = px.histogram(df, x='Numeros generados', color_discrete_sequence=['indianred'], nbins=cantidad_intervalos)
    return figure

if __name__ == "__main__":
    pass