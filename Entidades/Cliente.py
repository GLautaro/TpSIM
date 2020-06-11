class Cliente:
    def __init__(self, Maquina, estado, id):
        self.maquina = Maquina
        self.estado = estado
        self.id = id
    def __eq__(self, cliente):
        return self.id == cliente.id

class Mantenimiento(Cliente):
    def __init__(self, Maquina, estado, id):
        super().__init__(Maquina, estado, id)

    def __eq__(self, other):
        if other is None:
            return False
        if isinstance(other, Mantenimiento):
            return super().__eq__(self, other)

class Alumno(Cliente):
    def __init__(self, Maquina, estado, id):
        super().__init__(Maquina, estado, id)

    def __eq__(self, other):
        if other is None:
            return False
        if isinstance(other, Alumno):
            return super().__eq__(self, other)