class Evento:
    def __init__(self, duracion, nombre):
        self.duracion = duracion
        self.hora = controlador.reloj + duracion
        self.nombre = nombre
    
    def __gt__(self, evento):
        return self.hora > evento.hora

class LlegadaAlumno(Evento):
    def __init__(self, duracion, nombre):
        Evento.__init__(self, duracion, nombre)
        self.duracion = duracion
        self.hora = controlador.reloj + duracion
        self.nombre = nombre
    
    def calcularTiempoEntreLlegadas(self):
      # RND UNIFORME [A,B]
      return 2

class FinInscripcion(Evento):
    def __init__(self, duracion, nombre, Maquina):
        Evento.__init__(self, duracion, nombre)
        self.duracion = duracion
        self.hora = controlador.reloj + duracion
        self.nombre = nombre
        self.Maquina = Maquina