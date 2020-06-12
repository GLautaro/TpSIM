import pandas as pd
class Cliente:
    def __init__(self, Maquina, estado, id):
        self.maquina = Maquina
        self.estado = estado
        self.id = id

    def __eq__(self, cliente):
        return self.id == cliente.id

    def completarColumnas(self, df, nombre_col_estado, nombre_col_maquina, row):
        if nombre_col_estado in df.columns:
            df.at[row, nombre_col_estado] = self.estado
            df.at[row, nombre_col_maquina] = str(self.maquina.id_maquina) if self.maquina is not None else "*---------*"
        else:
            nones = [None for i in range(row)]
            df[nombre_col_estado] = nones + [self.estado]
            df[nombre_col_maquina] = nones + [str(self.maquina.id_maquina) if self.maquina is not None else "*---------*"]
        return df

class Mantenimiento(Cliente):
    def __init__(self, Maquina, estado, id):
        super().__init__(Maquina, estado, id)
        self.atendidas = []

    def fueMantenida(self,maquina):
        return maquina in self.atendidas

    def __eq__(self, other):
        if other is None:
            return False
        if isinstance(other, Mantenimiento):
            return super().__eq__(self, other)

    def agregarDF(self, df, row):
        nombre_col_estado = "Estado_mant_" + str(self.id)
        nombre_col_maquina = "Maquina_mant_" + str(self.id)
        return super().completarColumnas(df, nombre_col_estado, nombre_col_maquina, row)

class Alumno(Cliente):
    def __init__(self, Maquina, estado, id):
        super().__init__(Maquina, estado, id)

    def __eq__(self, other):
        if other is None:
            return False
        if isinstance(other, Alumno):
            return super().__eq__(self, other)

    def agregarDF(self, df, row):
        nombre_col_estado = "Estado_alum_" + str(self.id)
        nombre_col_maquina = "Maquina_alum_" + str(self.id)
        return super().completarColumnas(df, nombre_col_estado, nombre_col_maquina, row)