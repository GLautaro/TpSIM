class Cajero:
    def __init__(self, estado, id, tiempo_utilizacion, acum_t_utilizacion, cliente):
        self.id = id
        self.estado = estado
        self.cliente = cliente
        self.tiempo_utilizacion = tiempo_utilizacion
        self.acum_t_utilizacion = acum_t_utilizacion
    
    def __eq__(self, otro):
        if otro is None:
            return False
        if isinstance(otro, Maquina):
            return self.id_maquina == otro.id_maquina
        return False

    def finalizarAtencion(self):
        self.cliente = None
        self.estado = "Libre"
        # self.tiempo_utilizacion = tiempo_utilizacion
        # self.acum_t_utilizacion += tiempo_utilizacion

    def comenzarAtencion(self, cliente):
        self.cliente = cliente
        self.estado = "Siendo utilizado"

    def estaLibre(self):
        return self.estado == "Libre"