from Modulos.Utils import Truncate
import random

class Evento:
    def __init__(self, duracion, hora, nombre,reloj):
        self.duracion = duracion
        self.hora = reloj + duracion
        self.nombre = nombre
    
    def __gt__(self, evento):
        return self.hora > evento.hora

class LlegadaAlumno(Evento):
    def __init__(self, reloj, media_demora_insc):
        duracion = Truncate(random.expovariate(1/media_demora_insc), 4)
        hora = Truncate(reloj + duracion, 4)
        nombre = "Llegada Alumno"
        super().__init__(duracion, hora, nombre, reloj)
       
class FinInscripcion(Evento):
    def __init__(self, Maquina, reloj, a_insc, b_insc):
        duracion = Truncate(random.uniform(a_insc, b_insc), 4)
        hora = Truncate(reloj + duracion, 4)
        nombre = "Fin Inscripción"
        super().__init__(duracion, hora, nombre, reloj)
        self.Maquina = Maquina