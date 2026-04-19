import random

class BaseAgent:
    """
    Clase que modela un agente basico
    """

    def __init__(self, id, name):
        """
        Constructor del agente base:
            1. Asigna su identificador
            2. Asigna su nombre
        """

        self.id = id
        self.name = name

    def Name(self):
        """
        Metodo que devuelve el nombre del agente
        """

        return self.name
    
    def Id(self):
        """
        Metodo que devuelve el identificador del agente
        """

        return self.id
    
    def Start(self):
        """
        Metodo que se llama al iniciar el agente (Actualmente no hace nada)
        """

        print("Inicio del agente ")

    def Update(self, perception, map):
        """
        Metodo que se llama en cada actualizacion del agente (necesita percepcion y mapa):
            - Genera una accion aleatoria (numero del 0 al 4)
        Devuelve la accion y "True" (puede disparar siempre)
        """

        print("Toma de decisiones del agente")
        print(perception)

        print("Mapa")
        print(map)

        action = random.randint(0,4)

        return action, True
    
    def End(self, win):
        """
        Metodo que se llama al finalizar el agente, recibe el estado de terminacion ("Victoria" o "Derrota")
        """

        print("Agente finalizado")
        print("Victoria: ", win)