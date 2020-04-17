from openpyxl import Workbook,load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows

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
