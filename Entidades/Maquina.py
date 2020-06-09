class Maquina:
    def __init__(self, id_maquina, estado, acum_tiempo_inscripcion):
        self.id_maquina = id_maquina
        self.estado = estado
        self.acum_tiempo_inscripcion = 0

    def __eq__(self, otro):
        if isinstance(otro, Maquina):
            return self.id_maquina == otro.id_maquina
        return False