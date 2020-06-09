from Entidades.Cliente import Cliente, Alumno, Mantenimiento
from Entidades.Evento import Evento, LlegadaAlumno, FinInscripcion
from Entidades.Maquina import Maquina

class Controlador:
    def __init__(self, x, n, reloj):
        # x = Tiempo a simular
        # n = Cantidad de iteraciones
        self.reloj = reloj
        self.x = x
        self.n = n
        #Ver
        self.primer_llegada_alum = 2
        self.primer_llegada_mant = 60
        #
        self.cola = []
        self.acum_alumnos_retiran = 0
        self.acum_alumnos_llegaron = 0
        self.eventos = []
        self.alumnos = []
        self.array_fin_inscripcion = [0, 0, 0, 0, 0]
    
    def buscarMaquinaLibre(self):
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
    
    def buscarProximoEvento(self):
      return min(self.eventos)
    
    def buscarAlumno(self, maquina):
      for i in range(len(self.alumnos)):
        if self.alumnos[i].Maquina == maquina:
          return self.alumnos[i]
      return

    def crearVectorEstado(self, evento_actual):
        llegada_alumno = self.eventos[len(self.eventos) - 2]
        fin_inscripcion = self.eventos[len(self.eventos) - 1]
        return [evento_actual.nombre, self.reloj, llegada_alumno.duracion, llegada_alumno.hora, fin_inscripcion.duracion, self.array_fin_inscripcion[0], self.array_fin_inscripcion[1], self.array_fin_inscripcion[2], self.array_fin_inscripcion[3], self.array_fin_inscripcion[4], maquina1.estado, maquina2.estado, maquina3.estado, maquina4.estado, maquina5.estado, len(self.cola), self.acum_alumnos_retiran, self.acum_alumnos_llegaron, maquina1.acum_tiempo_inscripcion, maquina2.acum_tiempo_inscripcion, maquina3.acum_tiempo_inscripcion, maquina4.acum_tiempo_inscripcion, maquina5.acum_tiempo_inscripcion]

    def simular(self):
        for i in range(self.n): 
            print("\nIteracion: ", i)
            # ¿La hora actual es menor a la solicitada?
            if self.reloj < self.x:
                print("reloj: ", self.reloj)
                print("Cola: ", len(self.cola))
                evento_actual = self.buscarProximoEvento()
                print("Evento actual: ", evento_actual.nombre)
                self.eventos.remove(evento_actual)
                # Si el tipo de evento es una llegada de alumno:
                if isinstance(evento_actual, LlegadaAlumno):
                  llegada_alumno = LlegadaAlumno(0.5, "Llegada Alumno")
                  self.eventos.append(llegada_alumno)
                  self.acum_alumnos_llegaron+=1  
                  # ¿Hay menos de 4 alumnos en la cola?
                  if len(self.cola) < 4:
                      # ¿Hay alguna máquina libre?
                      maquina = self.buscarMaquinaLibre()
                      if maquina != None:
                          #Si hay ningún servidor libre                 
                          fin_inscripcion = FinInscripcion(5, "Fin de inscripción" ,maquina)
                          maquina.estado = "SIENDO_UTILIZADO"
                          self.array_fin_inscripcion[maquina.id_maquina] = fin_inscripcion.hora
                          maquina.acum_tiempo_inscripcion+= fin_inscripcion.duracion
                          alumno = Alumno(maquina, "SIENDO_INS")
                      else:
                          #Si no hay ningún servidor libre
                          print("Alumno ingresa a la cola")
                          alumno = Alumno(None, "ESPERANDO_INS")
                          self.cola.append(alumno)
                          fin_inscripcion = self.eventos[len(self.eventos) - 2]
                      self.alumnos.append(alumno)
                  #Si hay más de 4 alumnos en la cola
                  else:
                      print("Alumno se retira")
                      self.acum_alumnos_retiran+=1
                      fin_inscripcion = self.eventos[len(self.eventos) - 2]
                  self.eventos.append(fin_inscripcion)    
                #Si el tipo de evento es un fin de inscripción
                elif isinstance(evento_actual, FinInscripcion):
                    llegada_alumno = self.eventos[len(self.eventos) - 2]
                    self.eventos.append(llegada_alumno)
                    maquina = evento_actual.Maquina
                    alumno_finalizado = self.buscarAlumno(maquina)
                    alumno_finalizado.maquina = None
                    alumno_finalizado.estado = "-"
                    if len(self.cola) > 1:
                        self.cola.pop(0)
                        fin_inscripcion = FinInscripcion(5, "Fin de inscripción", maquina)
                        self.eventos.append(fin_inscripcion)
                        self.array_fin_inscripcion[maquina.id_maquina] = fin_inscripcion.hora
                        maquina.acum_tiempo_inscripcion+= fin_inscripcion.duracion
                        alumno = self.cola[0]
                        alumno.estado = "SIENDO_INS"
                        alumno.maquina = maquina
                        self.alumnos.append(alumno)
                        maquina.estado = "SIENDO_UTILIZADO"
                    else:
                        maquina.estado = "LIBRE"
                        self.array_fin_inscripcion[maquina.id_maquina] = 0
                #Vector de estado
                print(self.crearVectorEstado(evento_actual))
                #Incremetar reloj
                self.reloj = min(self.eventos).hora
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
controlador = Controlador(60, 5000, 0)
# parametro 1 = x = Tiempo a simular
# parametro 2 = n = Cantidad de iteraciones
# parametro 3 = reloj
controlador.reloj = min(controlador.primer_llegada_alum, controlador.primer_llegada_mant)
controlador.eventos.append(LlegadaAlumno(controlador.primer_llegada_alum, "Llegada alumno"))
controlador.simular()