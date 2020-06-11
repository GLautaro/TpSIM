from Entidades.Maquina import Maquina
from Entidades.Cliente import Cliente, Alumno, Mantenimiento
from Entidades.Evento import Evento, LlegadaAlumno, FinInscripcion, Inicializacion, LlegadaMantenimiento, FinMantenimiento
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
        self.mantenimientos = []
        self.array_fin_inscripcion = [0, 0, 0, 0, 0]
        self.array_fin_mantenimiento = [0, 0, 0, 0, 0]
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
    
    def buscarAlumno(self, maquina):
        '''
        La función recibe como parámetro un objeto máquina y retorna el alumno que tiene como atributo ese objeto. 
        '''
        for i in range(len(self.alumnos)):
          if self.alumnos[i].maquina == maquina:
            return self.alumnos[i]
        return
    
    def buscarMantenimiento(self, maquina):
        '''
        La función recibe como parámetro un objeto máquina y retorna el mantenimiento que tiene como atributo ese objeto. 
        '''
        for i in range(len(self.mantenimientos)):
          if self.mantenimientos[i].maquina == maquina:
            return self.mantenimientos[i]
        return

    def buscarMantenimientosEnCola(self):
        '''
        La función recibe como parámetro un objeto máquina y retorna el mantenimiento que tiene como atributo ese objeto. 
        '''
        for i in range(len(self.cola)):          
            if isinstance(self.cola[i], Mantenimiento):
                return self.cola[i]
        return

    def buscarSiguienteAtencion(self, maquina, contadorNumeroFin, vector_auxiliar):
        maquina.estado = "SIENDO UTILIZADO"
        cliente = self.buscarMantenimientosEnCola()
        if cliente != None:
            self.cola.remove(cliente)
            fin_mantenimiento = FinMantenimiento(maquina, self.reloj, self.media_demora_mant, self.desv_demora_mant, contadorNumeroFin-1)
            self.array_fin_mantenimiento[maquina.id_maquina-1] = fin_mantenimiento.hora
            fin_inscripcion = vector_auxiliar[2]
            cliente.estado, cliente.maquina = "REALIZANDO MANTENIMIENTO", maquina
        else:
            cliente = self.cola.pop(0)
            fin_inscripcion = FinInscripcion(maquina, self.reloj, self.a_insc, self.b_insc, contadorNumeroFin)
            self.array_fin_inscripcion[maquina.id_maquina-1] = fin_inscripcion.hora
            maquina.acum_tiempo_inscripcion+= fin_inscripcion.duracion
            maquina.acum_tiempo_inscripcion = Truncate(maquina.acum_tiempo_inscripcion, 2)
            fin_mantenimiento = vector_auxiliar[3]             
            cliente.estado, cliente.maquina = "SIENDO INSCRIPTO", maquina          
        self.eventos.append(fin_inscripcion)
        self.eventos.append(fin_mantenimiento)
        return fin_mantenimiento, fin_inscripcion, vector_auxiliar     
    
    def manejarCliente(self, cliente, contadorNumeroLlegada, vector_auxiliar):
        maquina = self.buscarMaquinaLibre() # ¿Hay alguna máquina libre?
        if maquina != None: #Si hay algún servidor libre            
            if isinstance(cliente, Alumno): 
                fin_inscripcion = FinInscripcion(maquina, self.reloj, self.a_insc, self.b_insc, contadorNumeroLlegada-1)                            
                self.array_fin_inscripcion[maquina.id_maquina-1] = fin_inscripcion.hora
                maquina.acum_tiempo_inscripcion+= fin_inscripcion.duracion
                maquina.acum_tiempo_inscripcion = Truncate(maquina.acum_tiempo_inscripcion, 2)
                cliente.estado = "SIENDO INSCRIPTO"
                fin_mantenimiento = vector_auxiliar[3]
                self.eventos.append(fin_inscripcion)
            if isinstance(cliente, Mantenimiento):
                fin_mantenimiento = FinMantenimiento(maquina, self.reloj, self.media_demora_mant, self.desv_demora_mant, contadorNumeroLlegada-1)
                self.array_fin_mantenimiento[maquina.id_maquina-1] = fin_mantenimiento.hora
                cliente.estado = "REALIZANDO MANTENIMIENTO"
                fin_inscripcion = vector_auxiliar[2]
                self.eventos.append(fin_mantenimiento)                       
            cliente.maquina = maquina
            maquina.estado = "SIENDO UTILIZADO"
        else: #Si no hay ningún servidor libre
            print("Cliente ingresa a la cola")
            cliente.maquina = None          
            if isinstance(cliente, Alumno): 
                cliente.estado = "ESPERANDO INSCRIPCIÓN"                
            if isinstance(cliente, Mantenimiento):
                cliente.estado = "ESPERANDO MANTENIMIENTO"
            fin_inscripcion = vector_auxiliar[2] #Repetir fin insc fila anterior
            fin_mantenimiento = vector_auxiliar[3]
            self.cola.append(cliente)
        return  fin_inscripcion, fin_mantenimiento                

    def manejarInicializacion(self):
        '''
        La función realiza las operaciones necesarias para el evento del tipo Inicialización
        '''
        llegada_alumno = LlegadaAlumno(self.reloj, self.media_llegada_al, 1)
        llegada_mantenimiento = LlegadaMantenimiento(self.reloj, self.media_llegada_mant, self.desv_llegada_mant, 1)
        fin_inscripcion = FinInscripcion(None, 0, 0, 0, 0)
        fin_mantenimiento = FinMantenimiento(None, 0, 0, 0, 0)
        self.eventos.append(llegada_alumno)
        self.eventos.append(llegada_mantenimiento)
        return llegada_alumno, llegada_mantenimiento, fin_inscripcion, fin_mantenimiento
    
    def manejarLlegadaAlumno(self, contadorNumeroLlegada, contadorAlumnos, evento_actual, vector_auxiliar):
        '''
        La función realiza las operaciones necesarias para el evento del tipo Llegada Alumno 
        '''
        llegada_alumno = LlegadaAlumno(self.reloj, self.media_llegada_al, contadorNumeroLlegada)
        self.eventos.append(llegada_alumno)
        self.acum_alumnos_llegaron+=1
        contadorAlumnos+= 1
        llegada_mantenimiento = vector_auxiliar[1]
        if len(self.cola) < 4: # ¿Hay menos de 4 alumnos en la cola?
            alumno = Alumno(None, "", contadorAlumnos)
            self.alumnos.append(alumno)
            fin_inscripcion, fin_mantenimiento = self.manejarCliente(alumno, contadorNumeroLlegada, vector_auxiliar)
        else:  #Si hay más de 4 alumnos en la cola
            print("Alumno se retira")
            self.acum_alumnos_retiran+=1
            evento_actual.hora += 30
            self.eventos.append(evento_actual)
            fin_inscripcion = vector_auxiliar[2] #Repetir fin insc fila anterior
            fin_mantenimiento = vector_auxiliar[3]
        return llegada_alumno, llegada_mantenimiento, fin_inscripcion, fin_mantenimiento, contadorAlumnos
    
    def manejarLlegadaMantenimiento(self, contadorNumeroLlegada, contadorMantenimientos, evento_actual, vector_auxiliar):
        '''
        La función realiza las operaciones necesarias para el evento del tipo Llegada Mantenimiento 
        '''
        llegada_mantenimiento = LlegadaMantenimiento(self.reloj, self.media_llegada_mant, self.desv_llegada_mant, contadorNumeroLlegada)
        self.eventos.append(llegada_mantenimiento)
        contadorMantenimientos += 1
        llegada_alumno = vector_auxiliar[0]
        mantenimiento = Mantenimiento(None, "", contadorMantenimientos)
        self.mantenimientos.append(mantenimiento)
        fin_inscripcion, fin_mantenimiento = self.manejarCliente(mantenimiento, contadorNumeroLlegada, vector_auxiliar)
        return llegada_alumno, llegada_mantenimiento, fin_inscripcion, fin_mantenimiento, contadorMantenimientos

    def manejarFinInscripcion(self, evento_actual, contadorNumeroFin, vector_auxiliar):
        '''
        La función realiza las operaciones necesarias para el evento del tipo Fin Inscripción
        '''
        llegada_alumno = vector_auxiliar[0]
        llegada_mantenimiento = vector_auxiliar[1]
        maquina = evento_actual.Maquina
        alumno_finalizado = self.buscarAlumno(maquina)
        alumno_finalizado.maquina = None
        alumno_finalizado.estado = "FINALIZADO"
        if len(self.cola) > 1:
            fin_mantenimiento, fin_inscripcion, vector_auxiliar  = self.buscarSiguienteAtencion(maquina, contadorNumeroFin, vector_auxiliar)
        else:
            maquina.estado = "LIBRE"
            self.array_fin_inscripcion[maquina.id_maquina-1] = 0
            fin_inscripcion = vector_auxiliar[2]
            fin_mantenimiento = vector_auxiliar[3]
        return llegada_alumno, llegada_mantenimiento, fin_inscripcion, fin_mantenimiento

    def manejarFinMantenimiento(self, evento_actual, contadorNumeroFin, vector_auxiliar):
        '''
        La función realiza las operaciones necesarias para el evento del tipo Fin Inscripción
        '''
        llegada_alumno = vector_auxiliar[0]
        llegada_mantenimiento = vector_auxiliar[1]
        maquina = evento_actual.Maquina
        mantenimiento_finalizado = self.buscarMantenimiento(maquina)
        mantenimiento_finalizado.maquina = None
        mantenimiento_finalizado.estado = "FINALIZADO"
        if len(self.cola) > 1:
            fin_mantenimiento, fin_inscripcion, vector_auxiliar  = self.buscarSiguienteAtencion(maquina, contadorNumeroFin, vector_auxiliar)
        else:
            maquina.estado = "LIBRE"
            self.array_fin_inscripcion[maquina.id_maquina-1] = 0
            fin_inscripcion = vector_auxiliar[2]
            fin_mantenimiento = vector_auxiliar[3]
        return llegada_alumno, llegada_mantenimiento, fin_inscripcion, fin_mantenimiento

    def crearVectorEstado(self, evento_actual,  llegada_alumno, fin_inscripcion, llegada_mantenimiento, fin_mantenimiento):
        '''
        La función recibe como parámetro el evento actual de la iteración y retorna el vector de estado correspondiente.
        '''
        lista = ["Evento Actual: " + str(evento_actual.nombre), 
                "Reloj: " + str(self.reloj), 
                "Tiempo entre llegadas alumno: " + str(llegada_alumno.duracion), 
                "Próxima llegada alumno: " + str(llegada_alumno.hora), 
                "Tiempo de inscripción: " + str(fin_inscripcion.duracion), 
                "Fin de inscripción 1: " + str(self.array_fin_inscripcion[0]), 
                "Fin de inscripción 2: " + str(self.array_fin_inscripcion[1]), 
                "Fin de inscripción 3: " + str(self.array_fin_inscripcion[2]), 
                "Fin de inscripción 4: " + str(self.array_fin_inscripcion[3]), 
                "Fin de inscripción 5: " + str(self.array_fin_inscripcion[4]),
                "Tiempo entre llegadas mantenimiento: " + str(llegada_mantenimiento.duracion), 
                "Próxima llegada mantenimiento: " + str(llegada_mantenimiento.hora),
                "Fin de mantenimiento 1: " + str(self.array_fin_inscripcion[0]), 
                "Fin de mantenimiento 2: " + str(self.array_fin_inscripcion[1]), 
                "Fin de mantenimiento 3: " + str(self.array_fin_inscripcion[2]), 
                "Fin de mantenimiento 4: " + str(self.array_fin_inscripcion[3]), 
                "Fin de mantenimiento 5: " + str(self.array_fin_inscripcion[4]),  
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
            lista.append("ID ALUMNO: " + str(a.id))
            lista.append(a.estado)
            m = a.maquina
            if m is None:
                m = "-"
            else:
                m = m.id_maquina
            lista.append(m)

        for a in self.mantenimientos:
            lista.append("ID MANT: " + str(a.id))
            lista.append(a.estado)
            m = a.maquina
            if m is None:
                m = "-"
            else:
                m = m.id_maquina
            lista.append(m)

        return lista

    def simular(self):
        contadorNumeroLlegadaAl = contadorNumeroFinIns = contadorNumeroLlegadaMant = contadorNumeroFinMant = 1
        contadorAlumnos = contadorMantenimientos = 0
        vector_auxiliar = [0, 0, 0, 0]
        inicializacion = Inicializacion() 
        self.eventos.append(inicializacion)
        for i in range(self.n): 
            print("\nIteracion: ", i)        
            evento_actual = min(self.eventos)
            self.eventos.remove(evento_actual)            
            if self.reloj < self.x: # ¿La hora actual es menor a la solicitada?

                if isinstance(evento_actual, Inicializacion):
                   llegada_alumno, llegada_mantenimiento, fin_inscripcion, fin_mantenimiento = self.manejarInicializacion()
                
                if isinstance(evento_actual, LlegadaAlumno): # Si el tipo de evento es una llegada de alumno
                    contadorNumeroLlegadaAl += 1  
                    llegada_alumno, llegada_mantenimiento, fin_inscripcion, fin_mantenimiento, contadorAlumnos = self.manejarLlegadaAlumno(contadorNumeroLlegadaAl, contadorAlumnos, evento_actual, vector_auxiliar)
                
                elif isinstance(evento_actual, LlegadaMantenimiento): # Si el tipo de evento es una llegada de mantenimiento
                    contadorNumeroLlegadaMant += 1
                    llegada_alumno, llegada_mantenimiento, fin_inscripcion, fin_mantenimiento, contadorMantenimientos = self.manejarLlegadaMantenimiento(contadorNumeroLlegadaMant, contadorMantenimientos, evento_actual, vector_auxiliar)
                
                elif isinstance(evento_actual, FinInscripcion):  #Si el tipo de evento es un fin de inscripción
                    contadorNumeroFinIns += 1
                    llegada_alumno, llegada_mantenimiento, fin_inscripcion, fin_mantenimiento = self.manejarFinInscripcion(evento_actual, contadorNumeroFinIns ,vector_auxiliar)
                
                elif isinstance(evento_actual, FinMantenimiento):  #Si el tipo de evento es un fin de mantenimiento
                    contadorNumeroFinMant += 1
                    llegada_alumno, llegada_mantenimiento, fin_inscripcion, fin_mantenimiento = self.manejarFinMantenimiento(evento_actual, contadorNumeroFinMant, vector_auxiliar)
                
                vector_auxiliar = [llegada_alumno, llegada_mantenimiento, fin_inscripcion, fin_mantenimiento]
                vector_estado = self.crearVectorEstado(evento_actual, llegada_alumno, fin_inscripcion, llegada_mantenimiento, fin_mantenimiento) #Vector de estado
                print(vector_estado)
                self.reloj = min(self.eventos).hora #Incremetar reloj
                self.reloj = Truncate(self.reloj, 2)
            else:
                break        
        print("\nacum alumnos que llegaron: ", self.acum_alumnos_llegaron)
        print("acum alumnos que se retiran: ", self.acum_alumnos_retiran)

def main():
    controlador = Controlador(400, 30, 0, 10, 15, 1, 60, 3, 3, 0.16)
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
    - Agregar RND en vector de estado
    - Test cuando el alumno se retira, ¿Hay que crear el objeto alumno?
    '''

if __name__ == "__main__":
    main()
