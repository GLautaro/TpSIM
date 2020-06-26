from Modulos.Constantes import EstadoAlumno as EA, EstadoMantenimiento as EM

class Cliente:
    def __init__(self, maquina, estado, id):
        self.id = id
        self.maquina = maquina
        self.estado = estado

    def __eq__(self, cliente):
        return self.id == cliente.id

    def completarColumnas(self, df, nombre_col_estado, nombre_col_maquina, row):
        if nombre_col_estado in df.columns:
            df.at[row, nombre_col_estado] = self.estado.value
            df.at[row, nombre_col_maquina] = str(self.maquina.id_maquina) if self.maquina is not None else "*---------*"
        else:
            nones = [None for i in range(row)]
            df[nombre_col_estado] = nones + [self.estado.value]
            df[nombre_col_maquina] = nones + [str(self.maquina.id_maquina) if self.maquina is not None else "*---------*"]
        return df

class Mantenimiento(Cliente):
    def __init__(self, maquina, estado, id):
        super().__init__(maquina, estado, id)

    def mantenerMaquina(self, maquina):
        self.estado = EM.MANTENIENDO_MAQU
        self.maquina = maquina
        maquina.realizarMantenimiento(self)

    def finalizarMantenimiento(self):
        self.estado = EM.FINALIZADO
        self.maquina.finalizarMantenimiento()
        self.maquina = None

    def comenzarEspera(self):
        self.estado = EM.ESPERANDO_MANT

    def __eq__(self, otro):
        if otro is None:
            return False
        if isinstance(otro, Mantenimiento):
            return super().__eq__(otro)

    def agregarDF(self, df, row):
        nombre_col_estado = "Estado_mant_" + str(self.id)
        nombre_col_maquina = "Maquina_mant_" + str(self.id)
        return super().completarColumnas(df, nombre_col_estado, nombre_col_maquina, row)

class Alumno(Cliente):
    def __init__(self, maquina, estado, id):
        super().__init__(maquina, estado, id)

    def comenzarInscripcion(self, maquina):
        self.estado = EA.SIENDO_INS
        self.maquina = maquina
        maquina.comenzarInscripcion(self)

    def finalizarInscripcion(self):
        self.estado = EA.FINALIZADO
        self.maquina.finalizarInscripcion()
        self.maquina = None

    def comenzarEspera(self):
        self.estado = EA.ESPERANDO_INS

    def retirarse(self):
        self.estado = EA.RETIRADO


    def __eq__(self, other):
        if other is None:
            return False
        if isinstance(other, Alumno):
            return super().__eq__(other)

    def agregarDF(self, df, row):
        nombre_col_estado = "Estado_alum_" + str(self.id)
        nombre_col_maquina = "Maquina_alum_" + str(self.id)
        return super().completarColumnas(df, nombre_col_estado, nombre_col_maquina, row)