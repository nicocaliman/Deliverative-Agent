from StateMachine.State import State
from States.AgentConsts import AgentConsts
import random

# TODO revisar si tiene que hacer algo mas
class RandomMovement(State):
    """
    Clase que genera un movimiento aleatorio
    """

    def __init__(self, id):
        """
        Constructora de la clase:
            - Llama al constructor de la clase superior ("State")
        """

        super().__init__(id)

    def Start(self, agent):
        """
        Inicia la clase:
            - Llama al metodo de la "Start" de la clase superior
            - Elige una accion aleatoria del 1 al 4
            - Reinicia el "updateTime"
        """

        super().Start(agent)
        self.action = random.randint(1, 4)
        self.updateTime = 0

    def Update(self, perception, map, agent):
        """
        Genera una accion aleatoria
        
        Devuelve una tupla (accion, "True")
        """

        self.action = random.randint(1,4)

        return self.action, True

    def Transit(self,perception, map):
        """
        Decide la transicion de estado en funcion de la accion tomada (NO HACE NADA)

        Devuelve el "id" del estado nuevo
        """
        
        self.updateTime += perception[AgentConsts.TIME]

        if self.updateTime > 1.0:
            return "ExecutePlan"
        
        return self.id
    