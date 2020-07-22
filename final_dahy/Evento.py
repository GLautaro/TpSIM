from Utils import Truncate
from Poisson import poisson
import random


class Evento:
    def __init__(self, duracion, hora, nombre, id):
        self.duracion = duracion
        self.hora = hora
        self.nombre = nombre
        self.id = id

    def __gt__(self, evento):
        return self.hora > evento.hora

    def __lt__(self, evento):
        return self.hora < evento.hora

class Inicializacion(Evento):
    def __init__(self):
        super().__init__(None, 0, "Inicialización", 0)

class FinSimulacion(Evento):
    def __init__(self, horaFin):
        super().__init__(None, horaFin, "Fin Simulacion", 0)

class LlegadaCliente(Evento):
    def __init__(self, reloj, media_llegada_cliente, id):
        duracion = Truncate(poisson(media_llegada_cliente))
        hora = Truncate((reloj + duracion), 2)
        nombre = "Llegada Cliente " + str(id)
        super().__init__(duracion, hora, nombre, id)

class FinAtencion(Evento):
    def __init__(self, cajero, reloj, media_fin, id):
        if media_fin != 0:
            duracion = Truncate(random.expovariate(1 / media_fin), 2)
        else:
            duracion = 0
        hora = Truncate((reloj + duracion), 2)
        nombre = "Fin Atención " + str(id)
        super().__init__(duracion, hora, nombre, id)
        self.cajero = cajero

class FinEspera(Evento):
    def __init__(self, horaFin):
        super().__init__(None, horaFin, "Fin espera", 0)
