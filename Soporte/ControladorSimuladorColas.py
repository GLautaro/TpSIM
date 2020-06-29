import os
from Modulos.Constantes import EstadoMaquinas as EM, TiposSimulacion as TS
from Modulos.TablasProbabilidad import CalcularCantidadArchivos,CrearProbabilidadesAcumuladas
from Soporte.EcDif import euler
import pandas as pd
import numpy as np
from Entidades.Maquina import Maquina
from Entidades.Cliente import Alumno, Mantenimiento
from Entidades.Evento import LlegadaAlumno, FinInscripcion, Inicializacion, LlegadaMantenimiento, \
    FinMantenimiento, FinSimulacion
from Modulos import Utils
from Modulos.Utils import Truncate


class Controlador:

    def __init__(self, x, reloj, a_insc, b_insc, media_llegada_al, a_mant, b_mant, media_demora_mant, desv_demora_mant,
                 mostrar_desde, mostrar_cantidad, tipo):
        '''
        x = Tiempo a simular
        n = Cantidad de iteraciones
        '''
        self.tipo = tipo
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

        self.contador_alumnos_llegaron = 0
        self.contador_alumnos_retiran = 0

        self.eventos = []
        self.alumnos = []
        self.mantenimientos = []

        self.array_fin_inscripcion = [0, 0, 0, 0, 0]
        self.array_fin_mantenimiento = [0, 0, 0, 0, 0]

        self.mostrar_desde_minuto = mostrar_desde
        self.mostrar_cantidad_iteraciones = mostrar_cantidad

        self.maquina1 = Maquina(1)
        self.maquina2 = Maquina(2)
        self.maquina3 = Maquina(3)
        self.maquina4 = Maquina(4)
        self.maquina5 = Maquina(5)

        self.llegada_alumno = None
        self.llegada_mantenimiento = None
        self.fin_inscripcion = None
        self.fin_mantenimiento = None

        self.contadorAlumnos = 1
        self.contadorMantenimientos = 1

        self.h = None
        self.probabilidades = None
        self.dict_integracion_numerica = {}
    def buscarMaquinaLibre(self):
        '''
        La función devuelve la primer máquina que encuentra en estado LIBRE
        '''
        libres = list(filter(lambda m: m.estaLibre(),
                             [self.maquina1, self.maquina2, self.maquina3, self.maquina4, self.maquina5]))
        if len(libres) == 0:
            return None
        else:
            return libres[0]

    def buscarMantenimientosEnCola(self):
        '''
        La función recibe como parámetro un objeto máquina y retorna el mantenimiento que tiene como atributo ese objeto.
        '''
        long = len(self.colaMantenimientos)
        if long == 0:
            return None
        elif long == 1:
            return self.colaMantenimientos[0]
        else:
            return min(self.colaMantenimientos, key=lambda x: x.id)

    def realizarMantenimiento(self, mantenimiento, maquina):
        if self.tipo == TS.TP5:
            fin_mantenimiento = FinMantenimiento(maquina, self.reloj, self.media_demora_mant, self.desv_demora_mant,
                                             mantenimiento.id)
        elif self.tipo == TS.TP6:
            fin_mantenimiento = FinMantenimiento(maquina, self.reloj, None, None,
                                                 mantenimiento.id,
                                                 self.probabilidades,
                                                 CalcularCantidadArchivos,
                                                 self.calcularTiempoSegunArchivos
                                                 )
        else:
            raise Exception("El tipo de simulacion cargado no es valido")
        self.array_fin_mantenimiento[maquina.id_maquina - 1] = fin_mantenimiento.hora
        mantenimiento.mantenerMaquina(maquina)
        self.eventos.append(fin_mantenimiento)
        self.fin_mantenimiento = fin_mantenimiento

    def buscarMaquinasNoMantenidas(self):
        maquinas_no_mantenidas = list(filter(lambda m: not m.estaMantenida(),
                                             [self.maquina1, self.maquina2, self.maquina3, self.maquina4,
                                              self.maquina5]))
        maquinas_no_mantenidas.sort(key=lambda x: x.acum_cant_mantenimientos)
        return maquinas_no_mantenidas

    def manejarInicializacion(self):
        '''
        La función realiza las operaciones necesarias para el evento del tipo Inicialización
        '''
        self.llegada_alumno = LlegadaAlumno(self.reloj, self.media_llegada_al, self.contadorAlumnos)
        self.llegada_mantenimiento = LlegadaMantenimiento(self.reloj, self.a_mant, self.b_mant,
                                                          self.contadorMantenimientos)

        self.fin_inscripcion = FinInscripcion(None, 0, 0, 0, 0)
        self.fin_mantenimiento = FinMantenimiento(None, 0, 0, 0, 0)
        self.eventos.append(self.llegada_alumno)
        self.eventos.append(self.llegada_mantenimiento)

    def manejarLlegadaAlumno(self, evento_actual):
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
        self.contador_alumnos_llegaron += 1
        self.contadorAlumnos += 1
        alumno = Alumno(None, "", evento_actual.id)
        self.alumnos.append(alumno)

        proxima_llegada_alumno = LlegadaAlumno(self.reloj, self.media_llegada_al, self.contadorAlumnos)
        self.eventos.append(proxima_llegada_alumno)
        self.llegada_alumno = proxima_llegada_alumno

        if len(self.cola) < 4:
            maquina = self.buscarMaquinaLibre()
            if maquina is not None:
                fin_inscripcion = FinInscripcion(maquina, self.reloj, self.a_insc, self.b_insc, alumno.id)
                self.eventos.append(fin_inscripcion)
                self.fin_inscripcion = fin_inscripcion
                self.array_fin_inscripcion[maquina.id_maquina - 1] = fin_inscripcion.hora
                alumno.comenzarInscripcion(maquina)
            else:
                self.cola.append(alumno)
                alumno.comenzarEspera()
        else:
            self.contador_alumnos_retiran += 1
            alumno.retirarse()

    def manejarLlegadaMantenimiento(self, evento_actual):
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
        self.contadorMantenimientos += 1
        mantenimiento = Mantenimiento(None, "", evento_actual.id)
        self.mantenimientos.append(mantenimiento)

        proxima_llegada_mantenimiento = LlegadaMantenimiento(self.reloj, self.a_mant, self.b_mant,
                                                             self.contadorMantenimientos)
        self.eventos.append(proxima_llegada_mantenimiento)
        self.llegada_mantenimiento = proxima_llegada_mantenimiento

        maquinas_no_mantenidas = self.buscarMaquinasNoMantenidas()
        maquina = None
        for m in maquinas_no_mantenidas:
            if m.estaLibre():
                maquina = m
                break

        if maquina is not None and self.buscarMantenimientosEnCola() is None:
            self.realizarMantenimiento(mantenimiento, maquina)
        else:
            mantenimiento.comenzarEspera()
            self.colaMantenimientos.append(mantenimiento)

    def manejarFinInscripcion(self, alumno_finalizado):
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
        maquina = alumno_finalizado.maquina
        alumno_finalizado.finalizarInscripcion()

        if len(self.colaMantenimientos) >= 1:
            maquina = None
            maquinas = self.buscarMaquinasNoMantenidas()
            for m in maquinas:
                if m.estaLibre():
                    maquina = m
            if maquina is not None:
                mantenimiento = self.buscarMantenimientosEnCola()
                self.realizarMantenimiento(mantenimiento, maquina)
                self.colaMantenimientos.remove(mantenimiento)
            elif len(self.cola) >= 1:
                maquina = self.buscarMaquinaLibre()
                alumno = self.cola.pop()
                fin_inscripcion = FinInscripcion(maquina, self.reloj, self.a_insc, self.b_insc, alumno.id)
                self.eventos.append(fin_inscripcion)
                self.fin_inscripcion = fin_inscripcion
                self.array_fin_inscripcion[maquina.id_maquina - 1] = fin_inscripcion.hora
                alumno.comenzarInscripcion(maquina)

        elif len(self.cola) >= 1:
            alumno = self.cola.pop()
            fin_inscripcion = FinInscripcion(maquina, self.reloj, self.a_insc, self.b_insc, alumno.id)
            self.eventos.append(fin_inscripcion)
            self.fin_inscripcion = fin_inscripcion
            self.array_fin_inscripcion[maquina.id_maquina - 1] = fin_inscripcion.hora
            alumno.comenzarInscripcion(maquina)

        else:
            self.array_fin_inscripcion[maquina.id_maquina - 1] = 0

    def manejarFinMantenimiento(self, mantenimiento_finalizado):
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
        maquina = mantenimiento_finalizado.maquina
        mantenimiento_finalizado.finalizarMantenimiento()

        if len(self.colaMantenimientos) >= 1:
            maquina = None
            maquinas = self.buscarMaquinasNoMantenidas()
            for m in maquinas:
                if m.estaLibre():
                    maquina = m
            if maquina is not None:
                mantenimiento = self.buscarMantenimientosEnCola()
                self.realizarMantenimiento(mantenimiento, maquina)
                self.colaMantenimientos.remove(mantenimiento)
            elif len(self.cola) >= 1:
                maquina = self.buscarMaquinaLibre()
                alumno = self.cola.pop()
                fin_inscripcion = FinInscripcion(maquina, self.reloj, self.a_insc, self.b_insc, alumno.id)
                self.eventos.append(fin_inscripcion)
                self.fin_inscripcion = fin_inscripcion
                self.array_fin_inscripcion[maquina.id_maquina - 1] = fin_inscripcion.hora
                alumno.comenzarInscripcion(maquina)

        elif len(self.cola) >= 1:
            alumno = self.cola.pop()
            fin_inscripcion = FinInscripcion(maquina, self.reloj, self.a_insc, self.b_insc, alumno.id)
            self.eventos.append(fin_inscripcion)
            self.fin_inscripcion = fin_inscripcion
            self.array_fin_inscripcion[maquina.id_maquina - 1] = fin_inscripcion.hora
            alumno.comenzarInscripcion(maquina)

        else:
            self.array_fin_mantenimiento[maquina.id_maquina - 1] = 0

    def crearVectorEstado(self, evento_actual):
        '''
        La función recibe como parámetro el evento actual de la iteración y retorna el vector de estado correspondiente.
        '''
        lista = ["Evento Actual: " + str(evento_actual.nombre),
                 "Reloj: " + str(self.reloj),
                 "Tiempo entre llegadas alumno: " + str(self.llegada_alumno.duracion),
                 "Próxima llegada alumno: " + str(self.llegada_alumno.hora),
                 "Tiempo de inscripción: " + str(self.fin_inscripcion.duracion),
                 "Fin de inscripción 1: " + str(self.array_fin_inscripcion[0]),
                 "Fin de inscripción 2: " + str(self.array_fin_inscripcion[1]),
                 "Fin de inscripción 3: " + str(self.array_fin_inscripcion[2]),
                 "Fin de inscripción 4: " + str(self.array_fin_inscripcion[3]),
                 "Fin de inscripción 5: " + str(self.array_fin_inscripcion[4]),
                 "Tiempo entre llegadas mantenimiento: " + str(self.llegada_mantenimiento.duracion),
                 "Próxima llegada mantenimiento: " + str(self.llegada_mantenimiento.hora),
                 "Fin de mantenimiento 1: " + str(self.array_fin_mantenimiento[0]),
                 "Fin de mantenimiento 2: " + str(self.array_fin_mantenimiento[1]),
                 "Fin de mantenimiento 3: " + str(self.array_fin_mantenimiento[2]),
                 "Fin de mantenimiento 4: " + str(self.array_fin_mantenimiento[3]),
                 "Fin de mantenimiento 5: " + str(self.array_fin_mantenimiento[4]),
                 "Maquina 1: " + str(self.maquina1.estado.value),
                 "Mantenimiento 1: " + str(self.maquina1.estado_mantenimiento.value),
                 "Maquina 2: " + str(self.maquina2.estado.value),
                 "Mantenimiento 2: " + str(self.maquina2.estado_mantenimiento.value),
                 "Maquina 3: " + str(self.maquina3.estado.value),
                 "Mantenimiento 3: " + str(self.maquina3.estado_mantenimiento.value),
                 "Maquina 4: " + str(self.maquina4.estado.value),
                 "Mantenimiento 4: " + str(self.maquina4.estado_mantenimiento.value),
                 "Maquina 5: " + str(self.maquina5.estado.value),
                 "Mantenimiento 5: " + str(self.maquina5.estado_mantenimiento.value),
                 "Cola alumnos: " + str(len(self.cola)),
                 "Cola Mantenimientos" + str(len(self.colaMantenimientos)),
                 "ACUM inscripciones Maquina 1: " + str(self.maquina1.acum_cant_inscripciones),
                 "ACUM inscripciones Maquina 2: " + str(self.maquina2.acum_cant_inscripciones),
                 "ACUM inscripciones Maquina 3: " + str(self.maquina3.acum_cant_inscripciones),
                 "ACUM inscripciones Maquina 4: " + str(self.maquina4.acum_cant_inscripciones),
                 "ACUM inscripciones Maquina 5: " + str(self.maquina5.acum_cant_inscripciones),
                 "Cantidad alumnos llegaron: " + str(self.contador_alumnos_llegaron),
                 "Cantidad alumnos retiran: " + str(self.contador_alumnos_retiran)
                 ]

        for a in self.alumnos:
            lista.append("ID ALUMNO: " + str(a.id))
            lista.append(a.estado.value)
            m = a.maquina
            if m is None:
                m = "-"
            else:
                m = m.id_maquina
            lista.append(m)

        for a in self.mantenimientos:
            lista.append("ID MANT: " + str(a.id))
            lista.append(a.estado.value)
            m = a.maquina
            if m is None:
                m = "-"
            else:
                m = m.id_maquina
            lista.append(m)

        return lista

    def crearVectorEstadoParcial(self, evento_actual):
        '''
        La función recibe como parámetro el evento actual de la iteración y retorna el vector de estado correspondiente.
        '''
        inicio_comunes = [
            str(evento_actual.nombre),
            str(self.reloj),
            str(self.llegada_alumno.duracion),
            str(self.llegada_alumno.hora),
            str(self.fin_inscripcion.duracion),
            str(self.array_fin_inscripcion[0]),
            str(self.array_fin_inscripcion[1]),
            str(self.array_fin_inscripcion[2]),
            str(self.array_fin_inscripcion[3]),
            str(self.array_fin_inscripcion[4]),
            str(self.llegada_mantenimiento.duracion),
            str(self.llegada_mantenimiento.hora)
        ]
        fin_comunes = [
            str(self.array_fin_mantenimiento[0]),
            str(self.array_fin_mantenimiento[1]),
            str(self.array_fin_mantenimiento[2]),
            str(self.array_fin_mantenimiento[3]),
            str(self.array_fin_mantenimiento[4]),
            str(self.maquina1.estado.value),
            str(self.maquina1.estado_mantenimiento.value),
            str(self.maquina2.estado.value),
            str(self.maquina2.estado_mantenimiento.value),
            str(self.maquina3.estado.value),
            str(self.maquina3.estado_mantenimiento.value),
            str(self.maquina4.estado.value),
            str(self.maquina4.estado_mantenimiento.value),
            str(self.maquina5.estado.value),
            str(self.maquina5.estado_mantenimiento.value),
            str(len(self.cola)),
            str(len(self.colaMantenimientos)),
            str(self.maquina1.acum_cant_inscripciones),
            str(self.maquina2.acum_cant_inscripciones),
            str(self.maquina3.acum_cant_inscripciones),
            str(self.maquina4.acum_cant_inscripciones),
            str(self.maquina5.acum_cant_inscripciones),
            str(self.contador_alumnos_llegaron),
            str(self.contador_alumnos_retiran)
        ]
        if self.tipo == TS.TP5:
            return inicio_comunes + [str(self.fin_mantenimiento.duracion)] + fin_comunes
        elif self.tipo == TS.TP6:
            return inicio_comunes + [self.fin_mantenimiento.rnd_archivos, self.fin_mantenimiento.cantidad, self.fin_mantenimiento.duracion_hyperlink] + fin_comunes
        else:
            raise Exception("El parametro introducido es invalido o alguno de ellos es nulo...")

    def crearColumnasParcialesDataFrame(self):
        '''
        Crea una lista con las columnas correspondientes a los datos siempre presentes en el dataframe
        '''
        inicio_comunes = [
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
            "Próxima llegada mantenimiento"
        ]
        fin_comunes = [
            "Tiempo mantenimiento",
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
            "Inscripciones Maquina 5",
            "Cantidad alumnos llegaron",
            "Cantidad alumnos retiran"
        ]
        if self.tipo == TS.TP5:
            return inicio_comunes + fin_comunes
        elif self.tipo == TS.TP6:
            return inicio_comunes + ["RND archivos", "Cantidad Archivos"] + fin_comunes
        else:
            raise Exception("El tipo de simulacion introducida es invalido...")

    def realizarIntegracionNumerica(self, h):
        for i in [1000, 1500, 2000]:
            self.dict_integracion_numerica[i] = euler(h, i, 0)

    def simular(self, paso_integracion=None, probabilidades_archivos=None):
        if self.tipo == TS.TP6:
            if paso_integracion is None or probabilidades_archivos is None:
                raise Exception("Los parametros no pueden ser None para el tipo de simulacion elegido...")
            self.realizarIntegracionNumerica(paso_integracion)
            self.probabilidades = CrearProbabilidadesAcumuladas(probabilidades_archivos)
        else:
            self.dict_integracion_numerica = None
        df_datos_fijos = pd.DataFrame(columns=self.crearColumnasParcialesDataFrame())
        df_alumnos = pd.DataFrame()
        df_manten = pd.DataFrame()

        inicializacion = Inicializacion()
        fin_simulacion = FinSimulacion(self.x)
        self.eventos.append(inicializacion)
        self.eventos.append(fin_simulacion)

        cantidad_iteraciones_mostradas = 0
        i = 0
        while self.reloj <= self.x:
            i += 1
            if len(self.buscarMaquinasNoMantenidas()) == 0:
                self.maquina1.estado_mantenimiento = EM.NO_MANTENIDA
                self.maquina2.estado_mantenimiento = EM.NO_MANTENIDA
                self.maquina3.estado_mantenimiento = EM.NO_MANTENIDA
                self.maquina4.estado_mantenimiento = EM.NO_MANTENIDA
                self.maquina5.estado_mantenimiento = EM.NO_MANTENIDA

            evento_actual = min(self.eventos, key=lambda x: x.hora)
            self.eventos.remove(evento_actual)  # Elimina el evento de la fila actual

            if isinstance(evento_actual, FinSimulacion):
                break

            if isinstance(evento_actual, Inicializacion):
                self.manejarInicializacion()

            if isinstance(evento_actual, LlegadaAlumno):  # Si el tipo de evento es una llegada de alumno
                self.manejarLlegadaAlumno(evento_actual)

            elif isinstance(evento_actual,
                            LlegadaMantenimiento):  # Si el tipo de evento es una llegada de mantenimiento
                self.manejarLlegadaMantenimiento(evento_actual)

            elif isinstance(evento_actual, FinInscripcion):  # Si el tipo de evento es un fin de inscripción
                self.manejarFinInscripcion(evento_actual.maquina.cliente)

            elif isinstance(evento_actual, FinMantenimiento):  # Si el tipo de evento es un fin de mantenimiento
                self.manejarFinMantenimiento(evento_actual.maquina.cliente)

            vector_estado = self.crearVectorEstado(evento_actual)  # Vector de estado
            print(vector_estado)
            if self.reloj >= self.mostrar_desde_minuto and cantidad_iteraciones_mostradas < self.mostrar_cantidad_iteraciones and cantidad_iteraciones_mostradas <= i:
                df_datos_fijos, df_alumnos, df_manten = self.agregarDatos(df_datos_fijos, df_alumnos, df_manten,
                                                                          evento_actual)
                cantidad_iteraciones_mostradas += 1

            self.reloj = min(self.eventos).hora  # Incrementar reloj
            self.reloj = Truncate(self.reloj, 2)

        df_datos_fijos, df_alumnos, df_manten = self.agregarDatos(df_datos_fijos, df_alumnos, df_manten, fin_simulacion)
        if self.tipo == TS.TP5:
            return df_datos_fijos.join(df_alumnos).join(df_manten), \
                   self.maquina1.acum_cant_inscripciones, \
                   self.maquina2.acum_cant_inscripciones, \
                   self.maquina3.acum_cant_inscripciones, \
                   self.maquina4.acum_cant_inscripciones, \
                   self.maquina5.acum_cant_inscripciones, \
                   self.contador_alumnos_llegaron, \
                   self.contador_alumnos_retiran
        elif self.tipo == TS.TP6 and self.dict_integracion_numerica is not None:
            dataframes = {"Simulacion": df_datos_fijos.join(df_alumnos).join(df_manten)}
            for k, v in self.dict_integracion_numerica.items():
                dataframes["Euler_" + str(k) + "_archivos"] = v
            return dataframes, \
                   self.maquina1.acum_cant_inscripciones, \
                   self.maquina2.acum_cant_inscripciones, \
                   self.maquina3.acum_cant_inscripciones, \
                   self.maquina4.acum_cant_inscripciones, \
                   self.maquina5.acum_cant_inscripciones, \
                   self.contador_alumnos_llegaron, \
                   self.contador_alumnos_retiran

    def agregarDatos(self, df_datos_fijos, df_alumnos, df_manten, evento_actual):
        vector_estado_parcial = self.crearVectorEstadoParcial(evento_actual)
        loc = len(df_datos_fijos)
        df_datos_fijos.loc[loc] = vector_estado_parcial
        for al in self.alumnos:
            df_alumnos = al.agregarDF(df_alumnos, loc)
        for m in self.mantenimientos:
            df_manten = m.agregarDF(df_manten, loc)
        return df_datos_fijos, df_alumnos, df_manten

    def calcularTiempoSegunArchivos(self, cantArchivos):
        df = self.dict_integracion_numerica[cantArchivos]
        df_aux = df.loc[df["A"] < 0]
        duracion = round(df_aux.iloc[0]["t"], 4)
        posicion = df_aux.index[0] + 2
        return duracion, posicion

def main(type):
    controlador = Controlador(4000,  # 1 x = Tiempo a simular
                              0,  # 2 reloj
                              0,  # 3 a_insc
                              5,  # 4 b_insc
                              15,  # 5 media_llegada_al
                              5,  # 6 a_mant
                              10,  # 7 b_mant
                              5,  # 8 media_demora_mant
                              3,  # 9 desv_demora_mant
                              0,  # 10 mostrar_desde_minuto
                              4000  # 11 mostrar_cantidad_iteraciones
                              )
    os.system("taskkill /F /IM excel.exe")
    if type == "1":
        respuesta = controlador.simular(TS.TP5)
        Utils.GenerarExcel({"Simulacion": respuesta[0]}, "tp6.xlsx")
    elif type == "2":
        respuesta = controlador.simular(TS.TP6)
        Utils.GenerarExcel(respuesta[0], "tp6.xlsx")
    else:
        raise Exception("El parametro ingresado es invalido...")
    os.startfile("tp5.xlsx")


'''
sacar parametro contador alumno y mantenimiento en funciones
'''

if __name__ == "__main__":
    ans = input("Elija el tipo de simulacion: \n"
                "TP5: Opcion uno. (1)\n"
                "TP6: Opcion dos. (2)\n")
    main(ans)
