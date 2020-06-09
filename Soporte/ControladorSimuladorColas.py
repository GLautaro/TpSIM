from Entidades.Cliente import Cliente, Alumno, Mantenimiento
from Entidades.Evento import Evento, LlegadaAlumno, FinInscripcion
from Entidades.Maquina import Maquina

class Controlador:
    def __init__(self, x, n, reloj, a_insc, b_insc, media_llegada_al, media_llegada_mant, desv_llegada_mant, media_demora_insc, desv_demora_insc):
        '''
        x = Tiempo a simular
        n = Cantidad de iteraciones
        '''
        self.reloj = reloj
        self.x = x
        self.n = n
        self.a_insc = a_insc
        self.b_insc = b_insc
        self.media_llegada_al = media_llegada_al
        self.media_llegada_mant = media_llegada_mant
        self.desv_llegada_mant = desv_llegada_mant
        self.media_demora_insc = media_demora_insc
        self.desv_demora_insc = desv_demora_insc
        self.primer_llegada_alum = 2 #Ver
        self.primer_llegada_mant = 60 #Ver
        self.cola = []
        self.acum_alumnos_retiran = 0
        self.acum_alumnos_llegaron = 0
        self.eventos = []
        self.alumnos = []
        self.array_fin_inscripcion = [0, 0, 0, 0, 0]
    
    def buscarMaquinaLibre(self):
        '''
        La función devuelve la primer máquina que encuentra en estado LIBRE 
        '''
        if maquina1.estado == 'LIBRE':
          return maquina1
        elif maquina2.estado == 'LIBRE':
          return maquina2
        elif maquina3.estado == 'LIBRE':
          return maquina3
        elif maquina4.estado == 'LIBRE':
          return maquina4
        elif maquina5.estado == 'LIBRE':
          return maquina5
        else:
          return None
    
    def manejarLlegadaAlumno(self):
        '''
        La función realiza las operaciones necesarias para el evento del tipo Llegada Alumno 
        '''
        llegada_alumno = LlegadaAlumno()
        self.eventos.append(llegada_alumno)
        self.acum_alumnos_llegaron+=1  
        if len(self.cola) <= 4: # ¿Hay menos de 4 alumnos en la cola?
            maquina = self.buscarMaquinaLibre() # ¿Hay alguna máquina libre?
            if maquina != None: #Si hay algún servidor libre 
                fin_inscripcion = FinInscripcion(maquina)
                maquina.estado = "SIENDO_UTILIZADO"
                self.array_fin_inscripcion[maquina.id_maquina] = fin_inscripcion.hora
                maquina.acum_tiempo_inscripcion+= fin_inscripcion.duracion
                alumno = Alumno(maquina, "SIENDO_INS")
            else: #Si no hay ningún servidor libre
                print("Alumno ingresa a la cola")
                alumno = Alumno(None, "ESPERANDO_INS")
                self.cola.append(alumno)
                fin_inscripcion = self.eventos[len(self.eventos) - 2] #Repetir fin insc fila anterior
            self.alumnos.append(alumno)
        else:  #Si hay más de 4 alumnos en la cola
            print("Alumno se retira")
            self.acum_alumnos_retiran+=1
            fin_inscripcion = self.eventos[len(self.eventos) - 2] #Repetir fin insc fila anterior
        self.eventos.append(fin_inscripcion) 
    
    def manejarFinInscripcion(self, evento_actual):
        '''
        La función realiza las operaciones necesarias para el evento del tipo Fin Inscripción
        '''
        llegada_alumno = self.eventos[len(self.eventos) - 2] #Repetir llegada alumno fila anterior
        self.eventos.append(llegada_alumno)
        maquina = evento_actual.Maquina
        alumno_finalizado = self.buscarAlumno(maquina)
        alumno_finalizado.maquina, alumno_finalizado.estado = None, "-"
        if len(self.cola) > 1:
            self.cola.pop(0)
            fin_inscripcion = FinInscripcion(maquina)
            self.eventos.append(fin_inscripcion)
            self.array_fin_inscripcion[maquina.id_maquina] = fin_inscripcion.hora
            maquina.acum_tiempo_inscripcion+= fin_inscripcion.duracion
            alumno = self.cola[0]
            alumno.estado, alumno.maquina, maquina.estado = "SIENDO_INS", maquina, "SIENDO_UTILIZADO"
            self.alumnos.append(alumno)
        else:
            maquina.estado = "LIBRE"
            self.array_fin_inscripcion[maquina.id_maquina] = 0

    def buscarAlumno(self, maquina):
        '''
        La función recibe como parámetro un objeto máquina y retorna el alumno que tiene como atributo ese objeto. 
        '''
        for i in range(len(self.alumnos)):
          if self.alumnos[i].Maquina == maquina:
            return self.alumnos[i]
        return

    def crearVectorEstado(self, evento_actual):
        '''
        La función recibe como parámetro el evento actual de la iteración y retorna el vector de estado correspondiente.
        '''
        llegada_alumno = self.eventos[len(self.eventos) - 2] #Busca el último evento del tipo llegada alumno ingresado en el vector eventos.
        fin_inscripcion = self.eventos[len(self.eventos) - 1] #Busca el último evento del tipo fin de inscripción ingresado en el vector eventos.
        return [evento_actual.nombre, self.reloj, llegada_alumno.duracion, llegada_alumno.hora, fin_inscripcion.duracion, self.array_fin_inscripcion[0], self.array_fin_inscripcion[1], self.array_fin_inscripcion[2], self.array_fin_inscripcion[3], self.array_fin_inscripcion[4], maquina1.estado, maquina2.estado, maquina3.estado, maquina4.estado, maquina5.estado, len(self.cola), self.acum_alumnos_retiran, self.acum_alumnos_llegaron, maquina1.acum_tiempo_inscripcion, maquina2.acum_tiempo_inscripcion, maquina3.acum_tiempo_inscripcion, maquina4.acum_tiempo_inscripcion, maquina5.acum_tiempo_inscripcion]

    def simular(self):
        for i in range(self.n): 
            print("\nIteracion: ", i)
            if self.reloj < self.x: # ¿La hora actual es menor a la solicitada?
                print("reloj: ", self.reloj)
                print("Cola: ", len(self.cola))
                evento_actual = min(self.eventos)
                print("Evento actual: ", evento_actual.nombre)
                self.eventos.remove(evento_actual)
                if isinstance(evento_actual, LlegadaAlumno): # Si el tipo de evento es una llegada de alumno:
                    self.manejarLlegadaAlumno()   
                elif isinstance(evento_actual, FinInscripcion):  #Si el tipo de evento es un fin de inscripción
                    self.manejarFinInscripcion(evento_actual)
                print(self.crearVectorEstado(evento_actual)) #Vector de estado
                self.reloj = min(self.eventos).hora #Incremetar reloj
            else:
                break
        print("\nacum alumnos que llegaron: ", self.acum_alumnos_llegaron)
        print("acum alumnos que se retiran: ", self.acum_alumnos_retiran)

#Inicialización
maquina1 = Maquina(0, "LIBRE", 0)
maquina2 = Maquina(1, "LIBRE", 0)
maquina3 = Maquina(2, "LIBRE", 0)
maquina4 = Maquina(3, "LIBRE", 0)
maquina5 = Maquina(4, "LIBRE", 0)
controlador = Controlador(60, 50, 0, 8, 5, 2, 1, 3, 3, 0.16)
#1 x = Tiempo a simular
#2 n = Cantidad de iteraciones
#3 reloj
#4 a_insc
#5 b_insc 
#6 media_llegada_al
#7 media_llegada_mant 
#8 desv_llegada_mant 
#9 media_demora_insc 
#10 desv_demora_insc
controlador.reloj = min(controlador.primer_llegada_alum, controlador.primer_llegada_mant)
controlador.eventos.append(LlegadaAlumno())
controlador.simular()
'''
DUDAS:
- cómo buscar alumno a finalizar sin usar un for
- qué hago en la fila en la que el alumno se retira
- cómo manejar los objetos alumnos en el vector de estado
- qué tengo que enviar en el front
'''