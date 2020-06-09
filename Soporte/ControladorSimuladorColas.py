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
        self.maquina1 = Maquina(0, "LIBRE", 0)
        self.maquina2 = Maquina(1, "LIBRE", 0)
        self.maquina3 = Maquina(2, "LIBRE", 0)
        self.maquina4 = Maquina(3, "LIBRE", 0)
        self.maquina5 = Maquina(4, "LIBRE", 0)
    
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
    
    def manejarLlegadaAlumno(self,contador):
        '''
        La función realiza las operaciones necesarias para el evento del tipo Llegada Alumno 
        '''
        llegada_alumno = LlegadaAlumno(self.reloj, self.media_demora_insc,contador)
        self.eventos.append(llegada_alumno)
        self.acum_alumnos_llegaron+=1  
        if len(self.cola) <= 4: # ¿Hay menos de 4 alumnos en la cola?
            maquina = self.buscarMaquinaLibre() # ¿Hay alguna máquina libre?
            if maquina != None: #Si hay algún servidor libre 
                fin_inscripcion = FinInscripcion(maquina,self.reloj,self.a_insc,self.b_insc,contador)
                maquina.estado = "SIENDO_UTILIZADO"
                self.array_fin_inscripcion[maquina.id_maquina] = fin_inscripcion.hora
                maquina.acum_tiempo_inscripcion+= fin_inscripcion.duracion
                alumno = Alumno(maquina, "SIENDO_INS")
            else: #Si no hay ningún servidor libre
                print("Alumno ingresa a la cola")
                alumno = Alumno(None, "ESPERANDO_INS")
                self.cola.append(alumno)
                fin_inscripcion = self.eventos[len(self.eventos) - 1] #Repetir fin insc fila anterior
            self.alumnos.append(alumno)
        else:  #Si hay más de 4 alumnos en la cola
            print("Alumno se retira")
            self.acum_alumnos_retiran+=1
            fin_inscripcion = self.eventos[len(self.eventos) - 1] #Repetir fin insc fila anterior
        self.eventos.append(fin_inscripcion)
    
    def manejarFinInscripcion(self, evento_actual,contador):
        '''
        La función realiza las operaciones necesarias para el evento del tipo Fin Inscripción
        '''
        llegada_alumno = self.eventos[len(self.eventos) - 2] #Repetir llegada alumno fila anterior
        self.eventos.append(llegada_alumno)
        maquina = evento_actual.Maquina
        alumno_finalizado = self.buscarAlumno(maquina)
        alumno_finalizado.maquina = None
        alumno_finalizado.estado = "FINALIZADO"
        if len(self.cola) > 1:
            alumno = self.cola.pop(0)
            fin_inscripcion = FinInscripcion(maquina,self.reloj,self.a_insc,self.b_insc,contador)
            self.array_fin_inscripcion[maquina.id_maquina] = fin_inscripcion.hora
            maquina.acum_tiempo_inscripcion+= fin_inscripcion.duracion
            alumno.estado, alumno.maquina, maquina.estado = "SIENDO_INS", maquina, "SIENDO_UTILIZADO"
            self.alumnos.append(alumno)
        else:
            maquina.estado = "LIBRE"
            self.array_fin_inscripcion[maquina.id_maquina] = 0
            fin_inscripcion = self.eventos[len(self.eventos) - 1]
        self.eventos.append(fin_inscripcion)

    def buscarAlumno(self, maquina):
        '''
        La función recibe como parámetro un objeto máquina y retorna el alumno que tiene como atributo ese objeto. 
        '''
        for i in range(len(self.alumnos)):
          if self.alumnos[i].maquina == maquina:
            return self.alumnos[i]
        return

    def crearVectorEstado(self, evento_actual):
        '''
        La función recibe como parámetro el evento actual de la iteración y retorna el vector de estado correspondiente.
        '''
        llegada_alumno = self.eventos[len(self.eventos) - 2] #Busca el último evento del tipo llegada alumno ingresado en el vector eventos.
        fin_inscripcion = self.eventos[len(self.eventos) - 1] #Busca el último evento del tipo fin de inscripción ingresado en el vector eventos.
        lista = [evento_actual.nombre, 
                self.reloj, 
                llegada_alumno.duracion, 
                llegada_alumno.hora, 
                fin_inscripcion.duracion, 
                self.array_fin_inscripcion[0], 
                self.array_fin_inscripcion[1], 
                self.array_fin_inscripcion[2], 
                self.array_fin_inscripcion[3], 
                self.array_fin_inscripcion[4], 
                self.maquina1.estado, 
                self.maquina2.estado, 
                self.maquina3.estado, 
                self.maquina4.estado, 
                self.maquina5.estado, 
                len(self.cola), 
                self.acum_alumnos_retiran, 
                self.acum_alumnos_llegaron, 
                self.maquina1.acum_tiempo_inscripcion, 
                self.maquina2.acum_tiempo_inscripcion, 
                self.maquina3.acum_tiempo_inscripcion, 
                self.maquina4.acum_tiempo_inscripcion, 
                self.maquina5.acum_tiempo_inscripcion
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
        for i in range(self.n): 
            print("\nIteracion: ", i)
            if self.reloj < self.x: # ¿La hora actual es menor a la solicitada?
                print("reloj: ", self.reloj)
                print("Cola: ", len(self.cola))
                evento_actual = min(self.eventos)
                print("Evento actual: ", evento_actual.nombre)
                self.eventos.remove(evento_actual)
                if isinstance(evento_actual, LlegadaAlumno): # Si el tipo de evento es una llegada de alumno:
                    self.manejarLlegadaAlumno(contadorNumeroLlegada)
                    contadorNumeroLlegada += 1   
                elif isinstance(evento_actual, FinInscripcion):  #Si el tipo de evento es un fin de inscripción
                    self.manejarFinInscripcion(evento_actual,contadorNumeroFin)
                    contadorNumeroFin += 1
                print(self.crearVectorEstado(evento_actual)) #Vector de estado
                self.reloj = min(self.eventos).hora #Incremetar reloj
            else:
                break
        print("\nacum alumnos que llegaron: ", self.acum_alumnos_llegaron)
        print("acum alumnos que se retiran: ", self.acum_alumnos_retiran)

def main():    
    #Inicialización
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
    controlador.eventos.append(LlegadaAlumno(controlador.reloj,controlador.media_demora_insc,1))
    controlador.simular()
    '''
    DUDAS:
    - cómo buscar alumno a finalizar sin usar un for: No se puede porque es una lista no ordenada
    - qué hago en la fila en la que el alumno se retira
    - cómo manejar los objetos alumnos en el vector de estado
    - qué tengo que enviar en el front: El front recibe un dataframe
    '''
if __name__ == "__main__":
    main()
