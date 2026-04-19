class State:
    """
    Clase que modela un "estado" del la maquina de estados
    """

    def __init__(self, id):
        """
        Constructora del estado:
            - Inicializa su id
        """

        self.id = id

    def Start(self, agent):
        """
        Metodo que se llama al iniciar el estado (NECESITA REIMPLEMENTACION EN OTRAS CLASES)
        """

        print("Inicio del estado ")

    def Update(self, perception, map, agent):
        """
        Metodo que se llama en cada actualizacion del estado (NECESITA REIMPLEMENTACION EN OTRAS CLASES)

        Devuelve las acciones del agente y si puede disparar o no
        """

        return 0, True
    
    def Transit(self, perception, map):
        """
        Metodo que se llama para decidir la trasicion del estado

        Devuelve el "id" del estado nuevo
        """

        return self.id
    
    def End(self):
        """
        Metodo que se llama al finalizar el estado
        """

        print("fin del estado")