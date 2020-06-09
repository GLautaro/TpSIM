from Modulos.Utils import Truncate

class Evento:
    def __init__(self, duracion, hora, nombre):
        self.duracion = duracion
        self.hora = controlador.reloj + duracion
        self.nombre = nombre
    
    def __gt__(self, evento):
        return self.hora > evento.hora

class LlegadaAlumno(Evento):
    def __init__(self):
        duracion = Truncate(random.expovariate(1/controlador.media_demora_insc), 4)
        hora = Truncate(controlador.reloj + duracion, 4)
        nombre = "Llegada Alumno"
        super().__init__(duracion, hora, nombre)
       
class FinInscripcion(Evento):
    def __init__(self, Maquina):
        duracion = Truncate(random.uniform(controlador.a_insc, controlador.b_insc), 4)
        hora = Truncate(controlador.reloj + duracion, 4)
        nombre = "Fin Inscripción"
        super().__init__(duracion, hora, nombre)
        self.Maquina = Maquina