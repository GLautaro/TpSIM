class Maquina:
    def __init__(self, id_maquina, estado, acum_cant_inscripciones, estado_mantenimiento, cliente):
        self.id_maquina = id_maquina
        self.estado = estado
        self.acum_cant_inscripciones = 0
        self.estado_mantenimiento = estado_mantenimiento
        self.cliente = cliente

    def __eq__(self, otro):
        if otro is None:
            return False
        if isinstance(otro, Maquina):
            return self.id_maquina == otro.id_maquina
        return False