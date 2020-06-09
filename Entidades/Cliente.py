class Cliente:
    def __init__(self, Maquina, estado):
        self.Maquina = Maquina
        self.estado = estado

class Mantenimiento(Cliente):
    def __init__(self, Maquina, estado):
        Cliente.__init__(self, Maquina, estado)
        self.Maquina = Maquina
        self.estado = estado

class Alumno(Cliente):
    def __init__(self, Maquina, estado):
        Cliente.__init__(self, Maquina, estado)
        self.Maquina = Maquina
        self.estado = estado     