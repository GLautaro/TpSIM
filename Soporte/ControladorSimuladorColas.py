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
        self.acum_alumnos_retiran = 0
        self.acum_alumnos_llegaron = 0
        self.eventos = []
        self.alumnos = []
        self.mantenimientos = []
        self.array_fin_inscripcion = [0, 0, 0, 0, 0]
        self.array_fin_mantenimiento = [0, 0, 0, 0, 0]
        self.mostrar_desde_minuto = mostrar_desde
        self.mostrar_cantidad_iteraciones = mostrar_cantidad
        self.maquina1 = Maquina(1, "LIBRE", 0, "NO MANTENIDA")
        self.maquina2 = Maquina(2, "LIBRE", 0, "NO MANTENIDA")
        self.maquina3 = Maquina(3, "LIBRE", 0, "NO MANTENIDA")
        self.maquina4 = Maquina(4, "LIBRE", 0, "NO MANTENIDA")
        self.maquina5 = Maquina(5, "LIBRE", 0, "NO MANTENIDA")

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
        for al in self.alumnos:
          if al.maquina == maquina:
            return al
        return

    def buscarMantenimiento(self, maquina):
        '''
        La función recibe como parámetro un objeto máquina y retorna el mantenimiento que tiene como atributo ese objeto.
        '''
        for man in self.mantenimientos:
          if man.maquina == maquina:
            return man
        return

    def buscarMantenimientosEnCola(self):
        '''
        La función recibe como parámetro un objeto máquina y retorna el mantenimiento que tiene como atributo ese objeto.
        '''
        for i in range(len(self.cola)):
            if isinstance(self.cola[i], Mantenimiento):
                return self.cola[i] #Falta retornar el objeto mantenimiento que ocurra primero
        return

    def buscarSiguienteAtencion(self, maquina, contadorNumeroFin, vector_auxiliar):
        '''
        La función se ejecuta cuando ocurre un evento de Fin de Inscripción o de Fin de mantenimiento, en donde el servidor se desocupa y aún exiten clientes en cola.
        Si existe algún cliente de mantenimiento, se le dará prioridad.
        '''
        maquina.estado = "SIENDO UTILIZADO"
        cliente = self.buscarMantenimientosEnCola()
        if cliente != None: #Si hay algún mantenimiento en cola
            self.cola.remove(cliente) #Elimina de la cola al cliente
            fin_mantenimiento = FinMantenimiento(maquina, self.reloj, self.media_demora_mant, self.desv_demora_mant, contadorNumeroFin-1)
            self.array_fin_mantenimiento[maquina.id_maquina-1] = fin_mantenimiento.hora
            fin_inscripcion = vector_auxiliar[2] #Busca el fin de inscripción de la fila anterior
            cliente.estado = "REALIZANDO MANTENIMIENTO"
            maquina.cliente = cliente
            cliente.maquina = maquina
            self.eventos.append(fin_mantenimiento)
        else:
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

    def manejarCliente(self, cliente, contadorNumeroLlegada, vector_auxiliar):
        '''
        La función realiza las operaciones necesarias para manejar los objetos clientes
        '''
        maquina = self.buscarMaquinaLibre() # ¿Hay alguna máquina libre?
        if maquina != None: #Si hay algún servidor libre
            if isinstance(cliente, Alumno):
                fin_inscripcion = FinInscripcion(maquina, self.reloj, self.a_insc, self.b_insc, contadorNumeroLlegada-1)
                self.array_fin_inscripcion[maquina.id_maquina-1] = fin_inscripcion.hora
                maquina.acum_cant_inscripciones += 1
                cliente.estado = "SIENDO INSCRIPTO"
                maquina.cliente = cliente
                fin_mantenimiento = vector_auxiliar[3]
                self.eventos.append(fin_inscripcion)
            if isinstance(cliente, Mantenimiento):
                fin_mantenimiento = FinMantenimiento(maquina, self.reloj, self.media_demora_mant, self.desv_demora_mant, contadorNumeroLlegada-1)
                self.array_fin_mantenimiento[maquina.id_maquina-1] = fin_mantenimiento.hora
                cliente.estado = "REALIZANDO MANTENIMIENTO"
                maquina.cliente = cliente
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
            fin_inscripcion = vector_auxiliar[2] #Busca el fin de inscripción de la fila anterior
            fin_mantenimiento = vector_auxiliar[3] #Busca el fin de mantenimiento de la fila anterior
            self.cola.append(cliente)
        return fin_inscripcion, fin_mantenimiento

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
        La función realiza las operaciones necesarias para el evento del tipo Llegada Alumno
        '''
        llegada_alumno = LlegadaAlumno(self.reloj, self.media_llegada_al, contadorNumeroLlegada)
        self.eventos.append(llegada_alumno)
        self.acum_alumnos_llegaron += 1
        contadorAlumnos += 1
        llegada_mantenimiento = vector_auxiliar[1]
        if len(self.cola) < 4: # ¿Hay menos de 4 alumnos en la cola?
            alumno = Alumno(None, "", contadorAlumnos)
            self.alumnos.append(alumno)
            fin_inscripcion, fin_mantenimiento = self.manejarCliente(alumno, contadorNumeroLlegada, vector_auxiliar)
        else:  #Si hay más de 4 alumnos en la cola
            print("Alumno se retira")
            self.acum_alumnos_retiran += 1
            evento_actual.hora += 30
            self.eventos.append(evento_actual)
            fin_inscripcion = vector_auxiliar[2] #Repetir fin insc fila anterior
            fin_mantenimiento = vector_auxiliar[3]
        return llegada_alumno, llegada_mantenimiento, fin_inscripcion, fin_mantenimiento, contadorAlumnos

    def manejarLlegadaMantenimiento(self, contadorNumeroLlegada, contadorMantenimientos, evento_actual, vector_auxiliar):
        '''
        La función realiza las operaciones necesarias para el evento del tipo Llegada Mantenimiento
        '''
        llegada_mantenimiento = LlegadaMantenimiento(self.reloj, self.a_mant, self.b_mant, contadorNumeroLlegada)
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
        maquina = evento_actual.maquina
        alumno_finalizado = maquina.cliente
        alumno_finalizado.maquina = None
        alumno_finalizado.estado = "FINALIZADO"
        if len(self.cola) >= 1:
            fin_mantenimiento, fin_inscripcion = self.buscarSiguienteAtencion(maquina, contadorNumeroFin, vector_auxiliar)
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
        maquina = evento_actual.maquina
        mantenimiento_finalizado = maquina.cliente
        mantenimiento_finalizado.maquina = None
        mantenimiento_finalizado.estado = "FINALIZADO"
        if len(self.cola) >= 1:
            fin_mantenimiento, fin_inscripcion = self.buscarSiguienteAtencion(maquina, contadorNumeroFin, vector_auxiliar)
        else:
            maquina.estado = "LIBRE"
            self.array_fin_mantenimiento[maquina.id_maquina-1] = 0
            fin_inscripcion = vector_auxiliar[2]
            fin_mantenimiento = vector_auxiliar[3]
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
                "Alumnos retiran: " + str(self.acum_alumnos_retiran),
                "Alumnos llegaron: " + str(self.acum_alumnos_llegaron),
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
                str(self.acum_alumnos_retiran),
                str(self.acum_alumnos_llegaron),
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
                 "Tiempo entre llegadasalumno",
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
                 "Alumnos retiran",
                 "Alumnos llegaron",
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
        
        while self.reloj <= self.x:
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
            if self.reloj >= self.mostrar_desde_minuto and cantidad_iteraciones_mostradas < self.mostrar_cantidad_iteraciones:
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
            
        return df_datos_fijos.join(df_alumnos).join(df_manten), self.acum_alumnos_llegaron, self.acum_alumnos_retiran

def main():
    controlador = Controlador(4000, 3000, 0, 10, 15, 5, 60, 3, 3, 0.16, 0, 200)

if __name__ == "__main__":
    main()
