from Entidades.Maquina import Maquina
from Entidades.Cliente import Cliente, Alumno, Mantenimiento
from Entidades.Evento import Evento, LlegadaAlumno, FinInscripcion, Inicializacion
from Modulos.Utils import Truncate

class Controlador:
    def __init__(self, x, n, reloj, a_insc, b_insc, media_llegada_al, media_llegada_mant, desv_llegada_mant, media_demora_mant, desv_demora_mant):
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
        self.media_demora_mant = media_demora_mant
        self.desv_demora_mant = desv_demora_mant
        self.cola = []
        self.acum_alumnos_retiran = 0
        self.acum_alumnos_llegaron = 0
        self.eventos = []
        self.alumnos = []
        self.array_fin_inscripcion = [0, 0, 0, 0, 0]
        self.maquina1 = Maquina(1, "LIBRE", 0)
        self.maquina2 = Maquina(2, "LIBRE", 0)
        self.maquina3 = Maquina(3, "LIBRE", 0)
        self.maquina4 = Maquina(4, "LIBRE", 0)
        self.maquina5 = Maquina(5, "LIBRE", 0)   

    def buscarMaquinaLibre(self):
        '''
        La función devuelve la primer máquina que encuentra en estado LIBRE 
        '''
        if self.maquina1.estado == 'LIBRE':
          return self.maquina1
        elif self.maquina2.estado == 'LIBRE':
          return self.maquina2
        elif self.maquina3.estado == 'LIBRE':
          return self.maquina3
        elif self.maquina4.estado == 'LIBRE':
          return self.maquina4
        elif self.maquina5.estado == 'LIBRE':
          return self.maquina5
        else:
          return None
    
    def manejarInicializacion(self):
        llegada_alumno = LlegadaAlumno(self.reloj, self.media_llegada_al, 1)
        fin_inscripcion = FinInscripcion(None, 0, 0, 0, 0)
        self.eventos.append(llegada_alumno)
        return llegada_alumno, fin_inscripcion
    
    def manejarLlegadaAlumno(self, contador, evento_actual):
        '''
        La función realiza las operaciones necesarias para el evento del tipo Llegada Alumno 
        '''
        llegada_alumno = LlegadaAlumno(self.reloj, self.media_llegada_al, contador)
        self.eventos.append(llegada_alumno)
        self.acum_alumnos_llegaron+=1  
        if len(self.cola) <= 4: # ¿Hay menos de 4 alumnos en la cola?
            maquina = self.buscarMaquinaLibre() # ¿Hay alguna máquina libre?
            print(maquina)
            if maquina != None: #Si hay algún servidor libre 
                fin_inscripcion = FinInscripcion(maquina, self.reloj, self.a_insc, self.b_insc, contador-1)
                self.eventos.append(fin_inscripcion)
                maquina.estado = "SIENDO UTILIZADO"
                self.array_fin_inscripcion[maquina.id_maquina-1] = fin_inscripcion.hora
                maquina.acum_tiempo_inscripcion+= fin_inscripcion.duracion
                maquina.acum_tiempo_inscripcion = Truncate(maquina.acum_tiempo_inscripcion, 2)
                alumno = Alumno(maquina, "SIENDO INSCRIPTO")
            else: #Si no hay ningún servidor libre
                print("Alumno ingresa a la cola")
                alumno = Alumno(None, "ESPERANDO INSCRIPCIÓN")
                self.cola.append(alumno)
                fin_inscripcion = self.eventos[len(self.eventos) - 1] #Repetir fin insc fila anterior
            self.alumnos.append(alumno)
        else:  #Si hay más de 4 alumnos en la cola
            print("Alumno se retira")
            self.acum_alumnos_retiran+=1
            evento_actual.hora += 30
            self.eventos.append(evento_actual)
            fin_inscripcion = self.eventos[len(self.eventos) - 1] #Repetir fin insc fila anterior
        return llegada_alumno, fin_inscripcion
    
    def manejarFinInscripcion(self, evento_actual, contador):
        '''
        La función realiza las operaciones necesarias para el evento del tipo Fin Inscripción
        '''
        llegada_alumno = self.eventos[len(self.eventos) - 2] #Repetir llegada alumno fila anterior
        maquina = evento_actual.Maquina
        alumno_finalizado = self.buscarAlumno(maquina)
        alumno_finalizado.maquina = None
        alumno_finalizado.estado = "FINALIZADO"
        if len(self.cola) > 1:
            alumno = self.cola.pop(0)
            fin_inscripcion = FinInscripcion(maquina, self.reloj, self.a_insc, self.b_insc, contador)
            self.eventos.append(fin_inscripcion)
            self.array_fin_inscripcion[maquina.id_maquina-1] = fin_inscripcion.hora
            maquina.acum_tiempo_inscripcion+= fin_inscripcion.duracion
            maquina.acum_tiempo_inscripcion = Truncate(maquina.acum_tiempo_inscripcion, 2)
            alumno.estado, alumno.maquina, maquina.estado = "SIENDO INSCRIPTO", maquina, "SIENDO UTILIZADO"
        else:
            maquina.estado = "LIBRE"
            self.array_fin_inscripcion[maquina.id_maquina-1] = 0
            fin_inscripcion = self.eventos[len(self.eventos) - 1]
        return llegada_alumno, fin_inscripcion

    def buscarAlumno(self, maquina):
        '''
        La función recibe como parámetro un objeto máquina y retorna el alumno que tiene como atributo ese objeto. 
        '''
        for i in range(len(self.alumnos)):
          if self.alumnos[i].maquina == maquina:
            return self.alumnos[i]
        return

    def crearVectorEstado(self, evento_actual,  llegada_alumno, fin_inscripcion):
        '''
        La función recibe como parámetro el evento actual de la iteración y retorna el vector de estado correspondiente.
        '''
        #llegada_alumno = self.eventos[len(self.eventos) - 2] #Busca el último evento del tipo llegada alumno ingresado en el vector eventos.
        #fin_inscripcion = self.eventos[len(self.eventos) - 1] #Busca el último evento del tipo fin de inscripción ingresado en el vector eventos.
        lista = ["Evento Actual: " + str(evento_actual.nombre), 
                "Reloj: " + str(self.reloj), 
                "Tiempo entre llegadas: " + str(llegada_alumno.duracion), 
                "Próxima llegada: " + str(llegada_alumno.hora), 
                "Tiempo de inscripción: " + str(fin_inscripcion.duracion), 
                "Fin de inscripción 1: " + str(self.array_fin_inscripcion[0]), 
                "Fin de inscripción 2: " + str(self.array_fin_inscripcion[1]), 
                "Fin de inscripción 3: " + str(self.array_fin_inscripcion[2]), 
                "Fin de inscripción 4: " + str(self.array_fin_inscripcion[3]), 
                "Fin de inscripción 5: " + str(self.array_fin_inscripcion[4]), 
                "Maquina 1: " + str(self.maquina1.estado), 
                "Maquina 2: " + str(self.maquina2.estado), 
                "Maquina 3: " + str(self.maquina3.estado), 
                "Maquina 4: " + str(self.maquina4.estado), 
                "Maquina 5: " + str(self.maquina5.estado), 
                "Cola: " + str(len(self.cola)),
                "Alumnos retiran: " + str(self.acum_alumnos_retiran), 
                "Alumnos llegaron: " + str(self.acum_alumnos_llegaron), 
                "ACUM Maquina 1: " + str(self.maquina1.acum_tiempo_inscripcion), 
                "ACUM Maquina 2: " + str(self.maquina2.acum_tiempo_inscripcion), 
                "ACUM Maquina 3: " + str(self.maquina3.acum_tiempo_inscripcion), 
                "ACUM Maquina 4: " + str(self.maquina4.acum_tiempo_inscripcion), 
                "ACUM Maquina 5: " + str(self.maquina5.acum_tiempo_inscripcion)
                ]

        for a in self.alumnos:
            lista.append(a.estado)
            m = a.maquina
            if m is None:
                m = "-"
            else:
                m = m.id_maquina
            lista.append(m)
        return lista

    def simular(self):
        contadorNumeroLlegada = 1
        contadorNumeroFin = 1
        inicializacion = Inicializacion() 
        self.eventos.append(inicializacion)
        for i in range(self.n): 
            print("\nIteracion: ", i)
            print("Listado de eventos: ")
            for j in self.eventos:
                print('-'+j.nombre)          
            evento_actual = min(self.eventos)
            self.eventos.remove(evento_actual)            
            if self.reloj < self.x: # ¿La hora actual es menor a la solicitada?
                if isinstance(evento_actual, Inicializacion):
                    llegada_alumno, fin_inscripcion = self.manejarInicializacion()
                if isinstance(evento_actual, LlegadaAlumno): # Si el tipo de evento es una llegada de alumno
                    contadorNumeroLlegada += 1  
                    llegada_alumno, fin_inscripcion = self.manejarLlegadaAlumno(contadorNumeroLlegada, evento_actual)
                elif isinstance(evento_actual, FinInscripcion):  #Si el tipo de evento es un fin de inscripción
                    contadorNumeroFin += 1
                    llegada_alumno, fin_inscripcion = self.manejarFinInscripcion(evento_actual,contadorNumeroFin)
                vector_estado = self.crearVectorEstado(evento_actual, llegada_alumno, fin_inscripcion) #Vector de estado
                print(vector_estado)
                self.reloj = min(self.eventos).hora #Incremetar reloj
                self.reloj = Truncate(self.reloj, 2)
            else:
                break
            print("Listado de eventos: ")
            for j in self.eventos:
                print('-'+j.nombre)            
        print("\nacum alumnos que llegaron: ", self.acum_alumnos_llegaron)
        print("acum alumnos que se retiran: ", self.acum_alumnos_retiran)

def main():
    controlador = Controlador(100, 1000, 0, 8, 5, 2, 1, 3, 3, 0.16)
    #1 x = Tiempo a simular
    #2 n = Cantidad de iteraciones
    #3 reloj
    #4 a_insc
    #5 b_insc 
    #6 media_llegada_al
    #7 media_llegada_mant 
    #8 desv_llegada_mant 
    #9 media_demora_mant 
    #10 desv_demora_mant   
    controlador.simular()
    ''' 
    FALTA
    - Revisar tiempo entre llegadas alumnos
    - Agregar RND en vector de estado
    '''

if __name__ == "__main__":
    main()
