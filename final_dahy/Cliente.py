class Cliente:
    def __init__(self, cajero, estado, id):
        self.id = id
        self.estado = estado
        self.cajero = cajero
    
    def comenzarAtencion(self, cajero):
        self.estado = "Siendo atendido"
        self.cajero = cajero
        cajero.comenzarAtencion(self)

    def finalizarAtencion(self):
        self.estado = "Finalizado"
        self.cajero.finalizarAtencion()
        self.cajero = None

    def comenzarEspera(self):
        self.estado = "Esperando atención"

    def retirarse(self):
        self.estado = "Retirado"

    def __eq__(self, other):
        if other is None:
            return False
        if isinstance(other, Alumno):
            def __eq__(self, cliente):
                return self.id == cliente.id
        return False

    def agregarDF(self, df, row):
        nombre_col_estado = "Estado" + str(self.id)
        nombre_col_cajero = "Cajero" + str(self.id)
        return super().completarColumnas(df, nombre_col_estado, nombre_col_cajero, row)

    def completarColumnas(self, df, nombre_col_estado, nombre_col_maquina, row):
        if nombre_col_estado in df.columns:
            df.at[row, nombre_col_estado] = self.estado.value
            df.at[row, nombre_col_maquina] = str(self.maquina.id_maquina) if self.maquina is not None else "*---------*"
        else:
            nones = [None for i in range(row)]
            df[nombre_col_estado] = nones + [self.estado.value]
            df[nombre_col_maquina] = nones + [str(self.maquina.id_maquina) if self.maquina is not None else "*---------*"]
        return df