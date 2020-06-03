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

class EstadoAlumno(Enum):
    SIENDO_INS = 0
    ESPERANDO_INS = 1

class TipoEvento(Enum):
    LLEGADA_ALUM = 0
    FIN_INS = 1
    LLEGADA_MANTEN = 2
    FIN_MANTEN = 3

class EstadoMaquinas(Enum):
    LIBRE = 0
    SIENDO_UTILIZADO = 1
    SIENDO_MANTENIDO = 2
    
