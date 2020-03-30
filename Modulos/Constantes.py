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