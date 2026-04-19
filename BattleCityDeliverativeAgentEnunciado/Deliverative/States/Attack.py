from StateMachine.State import State
from States.AgentConsts import AgentConsts

class Attack(State):
    """
    Clase que modela es estado de "ataque" del agente
    """

    def __init__(self, id):
        """
        Constructora de la clase:
            - Llama al constructor de la clase superior ("State")
            - Inicializa la direccion a la que mira a "-1"
            - Inicializa "timeInAttack" a "0"
        """

        super().__init__(id)
        self.timeInAttack = 0

    def Start(self, agent):
        """
        Inicia la clase:
            - Inicializa los valores igual que la constructora
        """

        self.timeInAttack = 0

    def Update(self, perception, map, agent):
        """
        Genera un movimiento si es necesario y dispara siempre:
            - Calcula la posicion del agente y del jugador
            - Si el jugador se mueve, el agente tambien
        Devuelve la tupla (move, "True")
        """

        playerX = perception[AgentConsts.PLAYER_X]
        playerY = perception[AgentConsts.PLAYER_Y]
        agentX = perception[AgentConsts.AGENT_X]
        agentY = perception[AgentConsts.AGENT_Y]

        dx = playerX - agentX
        dy = playerY - agentY

        # Hay mas diferencia horizontal
        if (abs(dx) > abs(dy)):
            # El agente esta mas a la derecha
            if dx < 0: move = AgentConsts.MOVE_LEFT
            # El agente esta mas a la izquierda
            else: move = AgentConsts.MOVE_RIGHT
        # Hay mas diferenia vertical
        elif (abs(dx) < abs(dy)):
            # El agente esta por encima
            if dy < 0: move = AgentConsts.MOVE_DOWN
            # El agente esta por debajo
            else: move = AgentConsts.MOVE_UP
        else: move = AgentConsts.NO_MOVE
        
        self.timeInAttack += 1
        
        return (move, True)

    def Transit(self,perception, map):
        """
        Decide la transicion de estado:
            - Si el target desaparece (jugador o "command_center"), pasa a "ExecutePlan"
            - Si el jugador se mueve muy lejos, pasa a "Chase"
            - Si no, permanece en "Attack"
        """
        
        playerX = perception[AgentConsts.PLAYER_X]
        playerY = perception[AgentConsts.PLAYER_Y]

        commandX = perception[AgentConsts.COMMAND_CENTER_X]
        commandY = perception[AgentConsts.COMMAND_CENTER_Y]
        
        if (playerX == -1 or playerY == -1) or (commandX == -1 or commandY == -1) or self.timeInAttack >= 8:
            return "ExecutePlan"
        
        return self.id