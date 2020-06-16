import pandas as pd
from Entidades.Maquina import Maquina
from Entidades.Cliente import Cliente, Alumno, Mantenimiento
from Entidades.Evento import Evento, LlegadaAlumno, FinInscripcion, Inicializacion, LlegadaMantenimiento, FinMantenimiento
from Modulos.Utils import Truncate,GenerarExcel

class Controlador:
    def __init__(self, x, reloj, a_insc, b_insc, media_llegada_al, a_mant, b_mant, media_demora_mant, desv_demora_mant,mostrar_desde,mostrar_cantidad):
        '''
        x = Tiempo a simular
        n = Cantidad de iteraciones
        '''
        self.reloj = reloj
        self.x = x
        self.a_insc = a_insc
        self.b_insc = b_insc
        self.media_llegada_al = media_llegada_al
        self.a_mant = a_mant
        self.b_mant = b_mant
        self.media_demora_mant = media_demora_mant
        self.desv_demora_mant = desv_demora_mant
        self.cola = []
        self.colaMantenimientos = []
        self.eventos = []
        self.alumnos = []
        self.mantenimientos = []
        self.array_fin_inscripcion = [0, 0, 0, 0, 0]
        self.array_fin_mantenimiento = [0, 0, 0, 0, 0]
        self.mostrar_desde_minuto = mostrar_desde
        self.mostrar_cantidad_iteraciones = mostrar_cantidad
        self.maquina1 = Maquina(1, "LIBRE", 0, "NO MANTENIDA", None)
        self.maquina2 = Maquina(2, "LIBRE", 0, "NO MANTENIDA", None)
        self.maquina3 = Maquina(3, "LIBRE", 0, "NO MANTENIDA", None)
        self.maquina4 = Maquina(4, "LIBRE", 0, "NO MANTENIDA", None)
        self.maquina5 = Maquina(5, "LIBRE", 0, "NO MANTENIDA", None)

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

    def buscarMantenimientosEnCola(self):
        '''
        La función recibe como parámetro un objeto máquina y retorna el mantenimiento que tiene como atributo ese objeto.
        '''
        for i in range(len(self.colaMantenimientos)):
            if isinstance(self.colaMantenimientos[i], Mantenimiento):
                return self.colaMantenimientos[i] #Falta retornar el objeto mantenimiento que ocurra primero
        return

    def realizarMantenimiento(self, mantenimiento, maquina, contadorNumeroFin):
        fin_mantenimiento = FinMantenimiento(maquina, self.reloj, self.media_demora_mant, self.desv_demora_mant, contadorNumeroFin-1)
        self.eventos.append(fin_mantenimiento)
        self.array_fin_mantenimiento[maquina.id_maquina-1] = fin_mantenimiento.hora           
        mantenimiento.estado = "REALIZANDO MANTENIMIENTO"
        mantenimiento.maquina = maquina 
        maquina.cliente = mantenimiento           
        maquina.estado = "SIENDO MANTENIDO"
        return fin_mantenimiento
    
    def buscarSiguienteAtencion(self, maquina, contadorNumeroFin, vector_auxiliar):
        '''
        La función se ejecuta cuando ocurre un evento de Fin de Inscripción o de Fin de mantenimiento, en donde el servidor se desocupa y aún exiten clientes en cola.
        Si existe algún cliente de mantenimiento en cola:
            - 
        '''
        cliente = self.buscarMantenimientosEnCola()
        if cliente != None:           
            self.colaMantenimientos.remove(cliente) #Elimina de la cola al cliente
            fin_inscripcion = vector_auxiliar[2]
            fin_mantenimiento = self.realizarMantenimiento(cliente, maquina, contadorNumeroFin)            
        else:
            maquina.estado = "SIENDO UTILIZADO"
            cliente = self.cola.pop(0) #Elimina de la cola al cliente
            fin_inscripcion = FinInscripcion(maquina, self.reloj, self.a_insc, self.b_insc, contadorNumeroFin)
            self.array_fin_inscripcion[maquina.id_maquina-1] = fin_inscripcion.hora
            maquina.acum_cant_inscripciones+= 1
            fin_mantenimiento = vector_auxiliar[3] #Busca el fin de mantenimiento de la fila anterior
            cliente.estado = "SIENDO INSCRIPTO"
            maquina.cliente = cliente
            cliente.maquina = maquina
        self.eventos.append(fin_inscripcion)
        return fin_mantenimiento, fin_inscripcion

    def buscarMaquinasNoMantenidas(self):
        maquinas_no_mantenidas = []
        if self.maquina1.estado_mantenimiento == 'NO MANTENIDA':
          maquinas_no_mantenidas.append(self.maquina1)
        if self.maquina2.estado_mantenimiento == 'NO MANTENIDA':
          maquinas_no_mantenidas.append(self.maquina2)
        if self.maquina3.estado_mantenimiento == 'NO MANTENIDA':
          maquinas_no_mantenidas.append(self.maquina3)
        if self.maquina4.estado_mantenimiento == 'NO MANTENIDA':
          maquinas_no_mantenidas.append(self.maquina4)
        if self.maquina5.estado_mantenimiento == 'NO MANTENIDA':
          maquinas_no_mantenidas.append(self.maquina5)
        return maquinas_no_mantenidas
    
    def manejarInicializacion(self):
        '''
        La función realiza las operaciones necesarias para el evento del tipo Inicialización
        '''
        llegada_alumno = LlegadaAlumno(self.reloj, self.media_llegada_al, 1)
        llegada_mantenimiento = LlegadaMantenimiento(self.reloj, self.a_mant, self.b_mant, 1)
        fin_inscripcion = FinInscripcion(None, 0, 0, 0, 0)
        fin_mantenimiento = FinMantenimiento(None, 0, 0, 0, 0)
        self.eventos.append(llegada_alumno)
        self.eventos.append(llegada_mantenimiento)
        return llegada_alumno, llegada_mantenimiento, fin_inscripcion, fin_mantenimiento

    def manejarLlegadaAlumno(self, contadorNumeroLlegada, contadorAlumnos, evento_actual, vector_auxiliar):
        '''
        La función realiza las operaciones necesarias para el evento del tipo Llegada Alumno:
        1. Clientes:
            - Alumno: Crea el objeto alumno asignandole su id a partir del contador de alumnos,
                      agrega el objeto alumno al vector alumnos.
            - Mantenimiento: No se crea ningún objeto.
        2. Eventos:
            - Llegada alumno: Crea el objeto Llegada Alumno y lo agrega al vector de eventos.
            - Llegada mantenimiento: Busca el último evento llegada de mantenimiento.
            - Fin de inscripción: 
                Si existe algún servidor libre:
                    - Crea el evento Fin de Inscripción y lo agrega al vector de eventos.
                    - Modifica la hora de fin de inscripción de la máquina correspondiente en el array_fin_inscripcion.
                    - Mofica el estado del objeto alumno.
                    - Modifica los atributos de la máquina.
                Si no existe algún servidor libre:
                    - Busca el último evento Fin de Inscripción.
                    - Agrega el cliente a la cola.
                    - Modifica el estado del objeto alumno.
            - Fin de mantenimiento: Busca el último evento fin de mantenimiento.
        3. Retorno: Todos los eventos actuales y el contador de alumnos.
        '''
        contadorAlumnos += 1 
        alumno = Alumno(None, "", contadorAlumnos)   
        self.alumnos.append(alumno)  
        llegada_alumno = LlegadaAlumno(self.reloj, self.media_llegada_al, contadorNumeroLlegada)
        self.eventos.append(llegada_alumno)
        llegada_mantenimiento = vector_auxiliar[1]
        maquina = self.buscarMaquinaLibre()
        if maquina != None: 
            fin_inscripcion = FinInscripcion(maquina, self.reloj, self.a_insc, self.b_insc, contadorNumeroLlegada-1)
            self.eventos.append(fin_inscripcion)
            self.array_fin_inscripcion[maquina.id_maquina-1] = fin_inscripcion.hora
            alumno.estado = "SIENDO INSCRIPTO"
            alumno.maquina = maquina
            maquina.cliente = alumno           
            maquina.estado = "SIENDO UTILIZADO"
        else:
            fin_inscripcion = vector_auxiliar[2]     
            self.cola.append(alumno) 
            alumno.estado = "ESPERANDO INSCRIPCIÓN"                   
        fin_mantenimiento = vector_auxiliar[3]       
        return llegada_alumno, llegada_mantenimiento, fin_inscripcion, fin_mantenimiento, contadorAlumnos

    def manejarLlegadaMantenimiento(self, contadorNumeroLlegada, contadorMantenimientos, evento_actual, vector_auxiliar):
        '''
        La función realiza las operaciones necesarias para el evento del tipo Llegada Mantenimiento:
        1. Clientes:
            - Alumno: No se crea ningún objeto.
            - Mantenimiento: Crea el objeto mantenimiento asignandole su id a partir del contador de mantenimientos,
                             agrega el objeto mantenimiento al vector mantenimientos.
        2. Eventos:
            - Llegada alumno: Busca el último evento llegada alumno.
            - Llegada mantenimiento: Crea el objeto Llegada Mantenimiento y lo agrega al vector de eventos.
            - Fin de inscripción: Busca el último evento fin de inscripción.
            - Fin de mantenimiento: 
                Si existe algún servidor libre:
                    - Crea el evento Fin de Inscripción y lo agrega al vector de eventos.
                    - Modifica la hora de fin de inscripción de la máquina correspondiente en el array_fin_mantenimiento.
                    - Mofica el estado del objeto mantenimiento.
                    - Modifica los atributos de la máquina.
                Si no existe algún servidor libre:
                    - Busca el último evento Fin de Inscripción.
                    - Agrega el cliente a la cola.
                    - Modifica el estado del objeto mantenimiento.
        3. Retorno: Todos los eventos actuales y el contador de mantenimientos.
        '''
        contadorMantenimientos += 1     
        mantenimiento = Mantenimiento(None, "", contadorMantenimientos)
        self.mantenimientos.append(mantenimiento)
        llegada_alumno = vector_auxiliar[0]
        llegada_mantenimiento = LlegadaMantenimiento(self.reloj, self.a_mant, self.b_mant, contadorNumeroLlegada)
        fin_inscripcion = vector_auxiliar[2] 
        self.eventos.append(llegada_mantenimiento)
        maquinas_no_mantenidas = self.buscarMaquinasNoMantenidas()
        maquina = None
        for i in range (len(maquinas_no_mantenidas)):
            if maquinas_no_mantenidas[i].estado == 'LIBRE':
                maquina = maquinas_no_mantenidas[i]
                break
        if  maquina != None:       
            fin_mantenimiento = self.realizarMantenimiento(mantenimiento, maquina, contadorNumeroLlegada)
        else:
            fin_mantenimiento = vector_auxiliar[3]
            self.colaMantenimientos.append(mantenimiento)
            mantenimiento.estado = "ESPERANDO MANTENIMIENTO"                 
        return llegada_alumno, llegada_mantenimiento, fin_inscripcion, fin_mantenimiento, contadorMantenimientos

    def manejarFinInscripcion(self, evento_actual, contadorNumeroFin, vector_auxiliar):
        '''
        La función realiza las operaciones necesarias para el evento del tipo Fin Inscripción:
        1. Clientes:
            - Alumno: Se mofican los atributos necesarios para finalizar la inscripción del alumno correspondiente.
            - Mantenimiento: No se modifica ningún objeto del tipo mantenimiento.
        2. Eventos:
            - Llegada alumno: Busca el último evento llegada alumno.
            - Llegada mantenimiento: Busca el último evento llegada mantenimiento.
            Si existen clientes en cola:
            - Fin de mantenimiento y fin de inscripción se obtienen de la función buscarSiguienteAtencion()
            Si no existen clientes en cola:
            - Fin de mantenimiento y fin de inscripción se repiten de la fila anterior.
            - Se modifica el estado de la máquina correspondiente.
            - Se modifica el array_fin_inscripcion de la máquina correspondiente.
        3. Retorno: Todos los eventos actuales.
        '''
        maquina = evento_actual.maquina
        maquina.acum_cant_inscripciones += 1
        alumno_finalizado = maquina.cliente
        alumno_finalizado.maquina = None
        alumno_finalizado.estado = "FINALIZADO"
        llegada_alumno = vector_auxiliar[0]
        llegada_mantenimiento = vector_auxiliar[1]        
        if len(self.cola) >= 1:
            fin_mantenimiento, fin_inscripcion = self.buscarSiguienteAtencion(maquina, contadorNumeroFin, vector_auxiliar)
        else:
            fin_inscripcion = vector_auxiliar[2]
            fin_mantenimiento = vector_auxiliar[3]
            maquina.estado = "LIBRE"
            self.array_fin_inscripcion[maquina.id_maquina-1] = 0            
        return llegada_alumno, llegada_mantenimiento, fin_inscripcion, fin_mantenimiento

    def manejarFinMantenimiento(self, evento_actual, contadorNumeroFin, vector_auxiliar):
        '''
        La función realiza las operaciones necesarias para el evento del tipo Fin Mantenimiento:
         1. Clientes:
            - Alumno:  No se modifica ningún objeto del tipo alumno.
            - Mantenimiento: Se mofican los atributos necesarios del mantenimiento correspondiente.
        2. Eventos:
            - Llegada alumno: Busca el último evento llegada alumno.
            - Llegada mantenimiento: Busca el último evento llegada mantenimiento.
            Si existen clientes en cola:
            - Fin de mantenimiento y fin de inscripción se obtienen de la función buscarSiguienteAtencion()
            Si no existen clientes en cola:
            - Fin de mantenimiento y fin de inscripción se repiten de la fila anterior.
            - Se modifica el estado de la máquina correspondiente.
            - Se modifica el array_fin_mantenimiento de la máquina correspondiente.
        3. Retorno: Todos los eventos actuales.
        '''
        maquina = evento_actual.maquina
        mantenimiento_finalizado = maquina.cliente
        mantenimiento_finalizado.maquina = None
        mantenimiento_finalizado.estado = "FINALIZADO"
        maquina.estado_mantenimiento = "MANTENIDO"
        llegada_alumno = vector_auxiliar[0]
        llegada_mantenimiento = vector_auxiliar[1]    
        if len(self.cola) >= 1 or len(self.colaMantenimientos) >= 1:
            fin_mantenimiento, fin_inscripcion = self.buscarSiguienteAtencion(maquina, contadorNumeroFin, vector_auxiliar)
        else:
            fin_inscripcion = vector_auxiliar[2]
            fin_mantenimiento = vector_auxiliar[3]
            maquina.estado = "LIBRE"
            self.array_fin_mantenimiento[maquina.id_maquina-1] = 0
        return llegada_alumno, llegada_mantenimiento, fin_inscripcion, fin_mantenimiento

    def crearVectorEstado(self, evento_actual,  llegada_alumno, fin_inscripcion, llegada_mantenimiento):
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
                "Fin de mantenimiento 1: " + str(self.array_fin_mantenimiento[0]),
                "Fin de mantenimiento 2: " + str(self.array_fin_mantenimiento[1]),
                "Fin de mantenimiento 3: " + str(self.array_fin_mantenimiento[2]),
                "Fin de mantenimiento 4: " + str(self.array_fin_mantenimiento[3]),
                "Fin de mantenimiento 5: " + str(self.array_fin_mantenimiento[4]),
                "Maquina 1: " + str(self.maquina1.estado),
                "Mantenimiento 1: " + str(self.maquina1.estado_mantenimiento),
                "Maquina 2: " + str(self.maquina2.estado),
                "Mantenimiento 2: " + str(self.maquina2.estado_mantenimiento),
                "Maquina 3: " + str(self.maquina3.estado),
                "Mantenimiento 3: " + str(self.maquina3.estado_mantenimiento),
                "Maquina 4: " + str(self.maquina4.estado),
                "Mantenimiento 4: " + str(self.maquina4.estado_mantenimiento),
                "Maquina 5: " + str(self.maquina5.estado),
                "Mantenimiento 5: " + str(self.maquina5.estado_mantenimiento),
                "Cola: " + str(len(self.cola)),
                "Cola Mantenimientos" + str(len(self.colaMantenimientos)),
                "ACUM inscripciones Maquina 1: " + str(self.maquina1.acum_cant_inscripciones),
                "ACUM inscripciones Maquina 2: " + str(self.maquina2.acum_cant_inscripciones),
                "ACUM inscripciones Maquina 3: " + str(self.maquina3.acum_cant_inscripciones),
                "ACUM inscripciones Maquina 4: " + str(self.maquina4.acum_cant_inscripciones),
                "ACUM inscripciones Maquina 5: " + str(self.maquina5.acum_cant_inscripciones)
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

    def crearVectorEstadoParcial(self, evento_actual,  llegada_alumno, fin_inscripcion, llegada_mantenimiento):
        '''
        La función recibe como parámetro el evento actual de la iteración y retorna el vector de estado correspondiente.
        '''
        return [
                str(evento_actual.nombre),
                str(self.reloj),
                str(llegada_alumno.duracion),
                str(llegada_alumno.hora),
                str(fin_inscripcion.duracion),
                str(self.array_fin_inscripcion[0]),
                str(self.array_fin_inscripcion[1]),
                str(self.array_fin_inscripcion[2]),
                str(self.array_fin_inscripcion[3]),
                str(self.array_fin_inscripcion[4]),
                str(llegada_mantenimiento.duracion),
                str(llegada_mantenimiento.hora),
                str(self.array_fin_mantenimiento[0]),
                str(self.array_fin_mantenimiento[1]),
                str(self.array_fin_mantenimiento[2]),
                str(self.array_fin_mantenimiento[3]),
                str(self.array_fin_mantenimiento[4]),
                str(self.maquina1.estado),
                str(self.maquina1.estado_mantenimiento),
                str(self.maquina2.estado),
                str(self.maquina2.estado_mantenimiento),
                str(self.maquina3.estado),
                str(self.maquina3.estado_mantenimiento),
                str(self.maquina4.estado),
                str(self.maquina4.estado_mantenimiento),
                str(self.maquina5.estado),
                str(self.maquina5.estado_mantenimiento),
                str(len(self.cola)),
                str(len(self.colaMantenimientos)),
                str(self.maquina1.acum_cant_inscripciones),
                str(self.maquina2.acum_cant_inscripciones),
                str(self.maquina3.acum_cant_inscripciones),
                str(self.maquina4.acum_cant_inscripciones),
                str(self.maquina5.acum_cant_inscripciones)
                ]

    def crearColumnasParcialesDataFrame(self):
        '''
        Crea una lista con las columnas correspondientes a los datos siempre presentes en el dataframe
        '''
        return [
                 "Evento Actual",
                 "Reloj",
                 "Tiempo entre llegadas alumno",
                 "Próxima llegada alumno",
                 "Tiempo inscripción",
                 "Fin inscripción 1",
                 "Fin inscripción 2",
                 "Fin inscripción 3",
                 "Fin inscripción 4",
                 "Fin inscripción 5",
                 "Tiempo entre llegadas mantenimiento",
                 "Próxima llegada mantenimiento",
                 "Fin mantenimiento 1",
                 "Fin mantenimiento 2",
                 "Fin mantenimiento 3",
                 "Fin mantenimiento 4",
                 "Fin mantenimiento 5",
                 "Máquina 1",
                 "Mantenimiento 1",
                 "Máquina 2",
                 "Mantenimiento 2",
                 "Máquina 3",
                 "Mantenimiento 3",
                 "Máquina 4",
                 "Mantenimiento 4",
                 "Máquina 5",
                 "Mantenimiento 5",
                 "Cola",
                 "Cola Mantenimientos",
                 "Inscripciones Maquina 1",
                 "Inscripciones Maquina 2",
                 "Inscripciones Maquina 3",
                 "Inscripciones Maquina 4",
                 "Inscripciones Maquina 5"
                 ]

    def simular(self):
        columnas_fijas = self.crearColumnasParcialesDataFrame()
        df_datos_fijos = pd.DataFrame(columns=columnas_fijas)
        df_alumnos = pd.DataFrame()
        df_manten = pd.DataFrame()
        contadorNumeroLlegadaAl = contadorNumeroFinIns = contadorNumeroLlegadaMant = contadorNumeroFinMant = 1
        contadorAlumnos = contadorMantenimientos = 0
        vector_auxiliar = [0, 0, 0, 0] #Se utiliza para poder obtener los eventos de la fila anterior
        inicializacion = Inicializacion()
        self.eventos.append(inicializacion)
        cantidad_iteraciones_mostradas = 0
        i = 0
        while self.reloj <= self.x:
            i+=1
            if self.buscarMaquinasNoMantenidas() == []:
                self.maquina1.estado_mantenimiento = "NO MANTENIDA"
                self.maquina2.estado_mantenimiento = "NO MANTENIDA"
                self.maquina3.estado_mantenimiento = "NO MANTENIDA"
                self.maquina4.estado_mantenimiento = "NO MANTENIDA"
                self.maquina5.estado_mantenimiento = "NO MANTENIDA"
            evento_actual = min(self.eventos)
            self.eventos.remove(evento_actual) #Elimina el evento de la fila actual
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
            vector_estado = self.crearVectorEstado(evento_actual, llegada_alumno, fin_inscripcion, llegada_mantenimiento) #Vector de estado
            print(vector_estado)
            if self.reloj >= self.mostrar_desde_minuto and cantidad_iteraciones_mostradas < self.mostrar_cantidad_iteraciones and cantidad_iteraciones_mostradas <= i:
                vector_estado_parcial = self.crearVectorEstadoParcial(evento_actual, llegada_alumno, fin_inscripcion, llegada_mantenimiento)
                loc = len(df_datos_fijos)
                df_datos_fijos.loc[loc] = vector_estado_parcial
                for al in self.alumnos:
                    df_alumnos = al.agregarDF(df_alumnos, loc)
                for m in self.mantenimientos:
                    df_manten = m.agregarDF(df_manten,loc)

                cantidad_iteraciones_mostradas += 1

            self.reloj = min(self.eventos).hora #Incrementar reloj
            self.reloj = Truncate(self.reloj, 2)     
            
        return df_datos_fijos.join(df_alumnos).join(df_manten), self.maquina1.acum_cant_inscripciones, self.maquina2.acum_cant_inscripciones, self.maquina3.acum_cant_inscripciones, self.maquina4.acum_cant_inscripciones, self.maquina5.acum_cant_inscripciones

def main():
    controlador = Controlador(4000, 0, 0, 10, 15, 5, 60, 3, 3, 0.16, 0)
    controlador.simular()
'''
sacar parametro contador alumno y mantenimiento en funciones
'''

if __name__ == "__main__":
    main()
