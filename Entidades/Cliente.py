

class Cliente():
    def __init__(self, horaInicio, estado, maquina):
        self.horaInicio = horaInicio
        self.estado = estado
        self.maquina = maquina       


class Alumno(Cliente):
    def inscribir(self):
        #TODO: Hacer enum estados alumno.
        self.estado = ""


class Mantenimiento(Cliente):
    def iniciarMantenimiento(self):
        #TODO: Hacer enum estados mantenimiento.
        self.estado = ""