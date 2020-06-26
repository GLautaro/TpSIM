from Modulos.Constantes import EstadoMaquinas as EM
class Maquina:
    def __init__(self, id_maquina):
        self.id_maquina = id_maquina
        self.estado = EM.COMUN_LIBRE
        self.acum_cant_inscripciones = 0
        self.acum_cant_mantenimientos = 0
        self.estado_mantenimiento = EM.NO_MANTENIDA
        self.cliente = None

    def __eq__(self, otro):
        if otro is None:
            return False
        if isinstance(otro, Maquina):
            return self.id_maquina == otro.id_maquina
        return False

    def finalizarInscripcion(self):
        self.cliente = None
        self.estado = EM.COMUN_LIBRE
        self.acum_cant_inscripciones += 1

    def comenzarInscripcion(self, alumno):
        self.cliente = alumno
        self.estado = EM.COMUN_SIENDO_UTILIZADA

    def finalizarMantenimiento(self):
        self.cliente = None
        self.estado = EM.COMUN_LIBRE
        self.acum_cant_mantenimientos += 1
        self.estado_mantenimiento = EM.MANTENIDA

    def realizarMantenimiento(self, mantenimiento):
        self.cliente = mantenimiento
        self.estado = EM.COMUN_SIENDO_MANTENIDA

    def estaMantenida(self):
        return self.estado_mantenimiento == EM.MANTENIDA

    def estaLibre(self):
        return self.estado == EM.COMUN_LIBRE


