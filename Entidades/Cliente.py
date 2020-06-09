class Cliente:
    def __init__(self, Maquina, estado):
        self.maquina = Maquina
        self.estado = estado

class Mantenimiento(Cliente):
    def __init__(self, Maquina, estado):
        super().__init__(Maquina, estado)

class Alumno(Cliente):
    def __init__(self, Maquina, estado):
        super().__init__(Maquina, estado)