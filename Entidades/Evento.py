from Modulos.Utils import Truncate
import random

class Evento:
    def __init__(self, duracion, hora, nombre):
        self.duracion = duracion
        self.hora = hora
        self.nombre = nombre
    
    def __gt__(self, evento):
        return self.hora > evento.hora

    def __lt__(self, evento):
        return self.hora < evento.hora

class Inicializacion(Evento):
    def __init__(self):
        duracion = None
        hora = None
        nombre = "Inicialización"
        super().__init__(duracion, hora, nombre)

class LlegadaAlumno(Evento):
    def __init__(self, reloj, media_llegada_alumno, contador):
        duracion = Truncate(random.expovariate(1/media_llegada_alumno), 2)
        hora = Truncate((reloj + duracion), 2)
        nombre = "Llegada Alumno " + str(contador)
        super().__init__(duracion, hora, nombre)
       
class FinInscripcion(Evento):
    def __init__(self, Maquina, reloj, a_insc, b_insc, contador):
        duracion = Truncate(random.uniform(a_insc, b_insc), 2)
        hora = Truncate((reloj + duracion), 2)
        nombre = "Fin Inscripción " + str(contador)
        super().__init__(duracion, hora, nombre)
        self.maquina = Maquina

class LlegadaMantenimiento(Evento):
    def __init__(self, reloj,media_llegada_mant, desv_llegada_mant, contador):
        duracion = Truncate(random.gauss(media_llegada_mant, desv_llegada_mant), 2)
        if duracion < 0:
            duracion = -duracion
        hora = Truncate((reloj + duracion), 2)
        nombre = "Llegada Mantenimiento " + str(contador)
        super().__init__(duracion, hora, nombre)
       
class FinMantenimiento(Evento):
    def __init__(self, Maquina, reloj, media_demora_mant, desv_demora_mant, contador):
        duracion = Truncate(random.gauss(media_demora_mant, desv_demora_mant), 2)
        if duracion < 0:
            duracion = -duracion
        hora = Truncate((reloj + duracion), 2)
        nombre = "Fin Mantenimiento " + str(contador)
        super().__init__(duracion, hora, nombre)
        self.maquina = Maquina