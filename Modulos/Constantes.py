#Archivo utilizado para definir las constantes utilizadas a lo largo de toda la aplicacion
#Se plantea para mejorar la legibilidad de codigo

from enum import Enum

class Intervalos(Enum):
    DIEZ = 10
    QUINCE = 15
    VEINTE = 20

class ResultadosChi2(Enum):
    H0_RECHAZADA = 0
    H0_NO_RECHAZABLE = 1

class EstadoMantenimiento(Enum):
    ESPERANDO_MANT = "ESPERANDO MANTENIMIENTO"
    MANTENIENDO_MAQU = "REALIZANDO MANTENIMIENTO"
    FINALIZADO = "FINALIZADO"

class EstadoAlumno(Enum):
    SIENDO_INS = "SIENDO INSCRIPTO"
    ESPERANDO_INS = "ESPERANDO INSCRIPCION"
    RETIRADO = "RETIRADO"
    FINALIZADO = "FINALIZADO"

class TipoEvento(Enum):
    LLEGADA_ALUM = 0
    FIN_INS = 1
    LLEGADA_MANTEN = 2
    FIN_MANTEN = 3

class EstadoMaquinas(Enum):
    COMUN_LIBRE = "LIBRE"
    COMUN_SIENDO_UTILIZADA = "SIENDO UTILIZADA"
    COMUN_SIENDO_MANTENIDA = "SIENDO MANTENIDA"
    MANTENIDA = "MANTENIDA"
    NO_MANTENIDA = "NO MANTENIDA"
    
