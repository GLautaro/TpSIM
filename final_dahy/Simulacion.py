import os
import pandas as pd
from Utils import Truncate
from Cajero import Cajero
from Cliente import Cliente
from Evento import Inicializacion, FinSimulacion, LlegadaCliente, FinAtencion, FinEspera

class Controlador:

    def __init__(self, cant_iteraciones, tiempo, mostrar_desde, media_llegada, media_fin):
        self.cajero1 = Cajero("Libre", 1, 0, 0, None)
        self.cajero2 = Cajero("Libre", 2, 0, 0, None)
        self.cajero3 = Cajero("Libre", 3, 0, 0, None)
        self.cajero4 = Cajero("Libre", 4, 0, 0, None)
        self.mostrar_cantidad_iteraciones = cant_iteraciones
        self.tiempo = tiempo
        self.mostrar_desde_minuto = mostrar_desde
        self.media_llegada = media_llegada
        self.media_fin = media_fin
        self.acum_tiempo_utilizacion = 0
        self.contador_clientes = 1
        self.reloj = 0
        self.eventos = []
        self.clientes = []
        self.cola = []
        self.array_fin_atencion = [0,0,0,0]

    def inicializacion(self):
        self.llegada_cliente = LlegadaCliente(self.reloj, self.media_llegada, self.contador_clientes)
        self.fin_atencion = FinAtencion(None, 0, 0, 0)
        self.eventos.append(self.llegada_cliente)

    def llegadaCliente(self, evento_actual):
        self.contador_clientes += 1
        cliente = Cliente(None, "", evento_actual.id)
        self.clientes.append(cliente)
        proxima_llegada_cliente = LlegadaCliente(self.reloj, self.media_llegada, self.contador_clientes)
        self.eventos.append(proxima_llegada_cliente)
        fin_espera = self.reloj + 5
        self.llegada_cliente = proxima_llegada_cliente
        cajero = self.buscarCajeroLibre()
        if cajero is not None:
            fin_atencion = FinAtencion(cajero, self.reloj, self.media_fin, cliente.id)
            self.eventos.append(fin_atencion)
            self.fin_atencion = fin_atencion
            self.array_fin_atencion[cajero.id - 1] = fin_atencion.hora
            cajero.comenzarAtencion(cliente)
            cliente.comenzarAtencion(cajero)
        else:
            self.cola.append(cliente)
            cliente.comenzarEspera()    

    def finAtencion(self, cajero, duracion):
        cliente_finalizado = cajero.cliente
        cliente_finalizado.finalizarAtencion()
        print("Cliente:", cliente_finalizado.id)
        print("Cajero:", cliente_finalizado.cajero)
        if len(self.cola) >= 1:
            cajero = self.buscarCajeroLibre()
            cliente = self.cola.pop()
            fin_atencion = FinAtencion(cajero, self.reloj, self.media_fin, cliente.id)
            self.eventos.append(fin_atencion)
            self.fin_atencion = fin_atencion
            self.array_fin_atencion[cajero.id - 1] = fin_atencion.hora
            cliente.comenzarAtencion(cajero)
        else:
            self.array_fin_atencion[cajero.id - 1] = 0

    def finEspera(self, cliente):
        if cola.index(cliente) >= 2:
            cliente.retirarse()
            self.llegada_cliente =  LlegadaCliente(self.reloj, self.media_llegada, cliente.id)
        return

    def buscarCajeroLibre(self):
        '''
        La función devuelve la primer máquina que encuentra en estado LIBRE
        '''
        libres = list(filter(lambda c: c.estaLibre(),
                             [self.cajero1, self.cajero2, self.cajero3, self.cajero4]))
        if len(libres) == 0:
            return None
        else:
            return libres[0]

    def crearVectorEstado(self, evento_actual):
        lista = ["Evento actual: " + str(evento_actual.nombre),
                 "Reloj: " + str(self.reloj),
                 "Tiempo entre llegadas:" + str(self.llegada_cliente.duracion),
                 "Próxima llegada: " + str(self.llegada_cliente.hora),
                 "Tiempo de atención: " + str(self.fin_atencion.duracion),
                 "Fin de atención 1: " + str(self.array_fin_atencion[0]),
                 "Fin de atención 2: " + str(self.array_fin_atencion[1]),
                 "Fin de atención 3: " + str(self.array_fin_atencion[2]),
                 "Fin de atención 4: " + str(self.array_fin_atencion[3]),
                 "Cajero 1: " + str(self.cajero1.estado),
                 "Cajero 2: " + str(self.cajero2.estado),
                 "Cajero 3: " + str(self.cajero3.estado),
                 "Cajero 4: " + str(self.cajero4.estado),
                 "Cola: " + str(len(self.cola)),
                 "Tiempo utilizacion 1: " + str(self.cajero1.tiempo_utilizacion),
                 "ACUM tiempo utilizacion 1: " + str(self.cajero1.acum_t_utilizacion),
                 "Tiempo utilizacion 2: " + str(self.cajero2.tiempo_utilizacion),
                 "ACUM tiempo utilizacion 2: " + str(self.cajero2.acum_t_utilizacion),
                 "Tiempo utilizacion 3: " + str(self.cajero3.tiempo_utilizacion),
                 "ACUM tiempo utilizacion 3: " + str(self.cajero3.acum_t_utilizacion),
                 "Tiempo utilizacion 4: " + str(self.cajero4.tiempo_utilizacion),
                 "ACUM tiempo utilizacion 4: " + str(self.cajero4.acum_t_utilizacion),                
                ]
        
        for c in self.clientes:
            lista.append("Cliente: " + str(c.id))
            lista.append(c.estado)
            cajero = c.cajero
            if cajero is None:
                cajero = "-"
            else:
                cajero = "Cajero: " + str(cajero.id)
            lista.append(cajero)
        return lista

    def crearVectorEstadoParcial(self, evento_actual):
        '''
        La función recibe como parámetro el evento actual de la iteración y retorna el vector de estado correspondiente.
        '''
        inicio_comunes = [
            str(evento_actual.nombre),
            str(self.reloj),
            str(self.llegada_cliente.duracion),
            str(self.llegada_cliente.hora),
            str(self.fin_atencion.duracion),
            str(self.array_fin_atencion[0]),
            str(self.array_fin_atencion[1]),
            str(self.array_fin_atencion[2]),
            str(self.array_fin_atencion[3]),
        ]
        fin_comunes = [
            str(self.cajero1.estado),
            str(self.cajero2.estado),
            str(self.cajero3.estado),
            str(self.cajero4.estado),
            str(len(self.cola)),
            str(self.cajero1.tiempo_utilizacion),
            str(self.cajero2.tiempo_utilizacion),
            str(self.cajero3.tiempo_utilizacion),
            str(self.cajero4.tiempo_utilizacion),
            str(self.cajero1.acum_t_utilizacion),
            str(self.cajero2.acum_t_utilizacion),
            str(self.cajero3.acum_t_utilizacion),
            str(self.cajero4.acum_t_utilizacion),
        ]

    def crearColumnasParcialesDataFrame(self):
        '''
        Crea una lista con las columnas correspondientes a los datos siempre presentes en el dataframe
        '''
        inicio_comunes = [
            "Evento Actual",
            "Reloj",
            "Tiempo entre llegadas",
            "Próxima llegada",
            "Tiempo atención",
            "Fin atención 1",
            "Fin atención 2",
            "Fin atención 3",
            "Fin atención 4",
        ]
        fin_comunes = [
            "Cajero 1",
            "Cajero 2",
            "Cajero 3",
            "Cajero 4",
            "Cola",
            "Tiempo utilización 1",
            "Tiempo utilización 2",
            "Tiempo utilización 3",
            "Tiempo utilización 4",
            "ACUM Tiempo utilización 1",
            "ACUM Tiempo utilización 2",
            "ACUMTiempo utilización 3",
            "ACUM Tiempo utilización 4",
        ]

    def agregarDatos(self, df_datos_fijos, df_clientes, evento_actual):
        vector_estado_parcial = self.crearVectorEstadoParcial(evento_actual)
        loc = len(df_datos_fijos)
        df_datos_fijos.loc[loc] = vector_estado_parcial
        for al in self.cldf_clientes:
            df_clientes = al.agregarDF(df_clientes, loc)
        return df_datos_fijos, df_clientes
    
    def simular(self):
        df_datos_fijos = pd.DataFrame(columns = self.crearColumnasParcialesDataFrame())
        df_clientes = pd.DataFrame()
        inicializacion = Inicializacion()
        fin_simulacion = FinSimulacion(self.tiempo)
        self.eventos.append(inicializacion)
        cant_iteraciones_mostradas = 0
        i=0
        while self.reloj <= self.tiempo:
            i += 1
            evento_actual = min(self.eventos, key=lambda x: x.hora)
            print(self.eventos)
            print("Evento actual: ", evento_actual.nombre)
            self.eventos.remove(evento_actual)

            if isinstance(evento_actual, FinSimulacion):
                break

            if isinstance(evento_actual, Inicializacion):
                self.inicializacion()

            if isinstance(evento_actual, LlegadaCliente): 
                self.llegadaCliente(evento_actual)

            elif isinstance(evento_actual, FinAtencion):  
                self.finAtencion(evento_actual.cajero, evento_actual.duracion)
            
            elif isinstance(evento_actual, FinEspera):
                self.finEspera(evento_actual.cajero.cliente)

            vector_estado = self.crearVectorEstado(evento_actual)
            print(vector_estado)
            if self.reloj >= self.mostrar_desde_minuto and cantidad_iteraciones_mostradas < self.mostrar_cantidad_iteraciones and cantidad_iteraciones_mostradas <= i:
                df_datos_fijos, df_alumnos, df_manten = self.agregarDatos(df_datos_fijos, df_clientes, evento_actual)
                cantidad_iteraciones_mostradas += 1
            self.reloj = min(self.eventos).hora
            self.reloj = Truncate(self.reloj, 2)
        
        df_datos_fijos, df_clientes = self.agregarDatos(df_datos_fijos, df_clientes, fin_simulacion)
        return df_datos_fijos.join(df_clientes)

