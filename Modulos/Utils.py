from openpyxl import Workbook,load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd
import numpy as np
def Truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

def GenerarExcel(dict_dataframes, nombre_archivo):
    wb = Workbook(nombre_archivo)
    for nombre,df in dict_dataframes.items():
        ws = wb.create_sheet(nombre)
        for r in dataframe_to_rows(df, index=False, header=True):
            ws.append(r)
    wb.save(nombre_archivo)

def ValidarVectorProbabilidades(vector):
    return (sum(vector) == 1)

def CrearDataFrame(ron, datos):
    col = ["Iteracion"]
    for i in range(ron):
        t1 = "ronda"+str(i+1)+"_tirada1"
        t2 = "ronda"+str(i+1)+"_tirada2"
        ##pun_t1 = t1+"_punt"
        ##pun_t2 = t2+"_punt"
        ran_t1 = "rand_" + t1
        rand_t2 = "rand_" + t2
        ##ac_t1 = pun_t1 + "_ac" 
        ##ac_t2 = pun_t2 + "_ac"
        ac_rond = "ronda_"+str(i+1)+"_punt_ac"
        col = col + [ran_t1,t1,rand_t2,t2,ac_rond]
    ##col = col + ["puntaje_final"]
    d = {}
    for c in col:
        d[c] = ["null","null1","null2"]

    df = pd.DataFrame(np.array(datos),columns=col)
    return df

    