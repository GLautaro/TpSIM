from Modulos.Utils import Truncate
from Modulos.Constantes import TiposSimulacion as TS
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


class LlegadaAlumno(Evento):
    def __init__(self, reloj, media_llegada_alumno, id):
        duracion = Truncate(random.expovariate(1 / media_llegada_alumno), 2)
        hora = Truncate((reloj + duracion), 2)
        nombre = "Llegada Alumno " + str(id)
        super().__init__(duracion, hora, nombre, id)


class FinInscripcion(Evento):
    def __init__(self, maquina, reloj, a_insc, b_insc, id):
        duracion = Truncate(random.uniform(a_insc, b_insc), 2)
        hora = Truncate((reloj + duracion), 2)
        nombre = "Fin Inscripción " + str(id)
        super().__init__(duracion, hora, nombre, id)
        self.maquina = maquina


class LlegadaMantenimiento(Evento):
    def __init__(self, reloj, a, b, id):
        duracion = Truncate(random.uniform(a, b), 2)
        if duracion < 0:
            duracion = -duracion
        hora = Truncate((reloj + duracion), 2)
        nombre = "Llegada Mantenimiento " + str(id)
        super().__init__(duracion, hora, nombre, id)


class FinMantenimiento(Evento):
    def __init__(self, maquina, reloj, media_demora_mant, desv_demora_mant, id, probabilidades=None, calcularCantidadArchivos=None, calcularTiempo=None):
        nombre = "Fin Mantenimiento " + str(id)

        if calcularCantidadArchivos is None and probabilidades is None and calcularTiempo is None:
            tipo = TS.TP5
            duracion = Truncate(random.gauss(media_demora_mant, desv_demora_mant), 2)
            if duracion < 0:
                duracion = -duracion
            hora = Truncate((reloj + duracion), 2)
        else:
            tipo = TS.TP6
            rnd_archivos = Truncate(random.uniform(0, 1.00001), 2)
            cantidad = calcularCantidadArchivos(probabilidades, rnd_archivos)
            duracion, posicion = calcularTiempo(cantidad)
            hora = Truncate((reloj + duracion), 2)
        super().__init__(duracion, hora, nombre, id)
        self.maquina = maquina
        if tipo == TS.TP6:
            self.duracion_hyperlink = '=HYPERLINK("#\'{0}\'!{1}{2}", {3})'.format("Euler_{0}_archivos".format(cantidad), "A", posicion, duracion)
            self.rnd_archivos = rnd_archivos
            self.cantidad = cantidad
        else:
            self.duracion_hyperlink = ""
            self.rnd_archivos = ""
            self.cantidad = ""