class Cliente:
    def __init__(self, Maquina, estado, id):
        self.maquina = Maquina
        self.estado = estado
        self.id = id

class Mantenimiento(Cliente):
    def __init__(self, Maquina, estado, id):
        super().__init__(Maquina, estado, id)

class Alumno(Cliente):
    def __init__(self, Maquina, estado, id):
        super().__init__(Maquina, estado, id)

