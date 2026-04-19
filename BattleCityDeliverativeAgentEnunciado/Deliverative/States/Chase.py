from StateMachine.State import State
from States.AgentConsts import AgentConsts
 
class Chase(State):
    """
    Clase que persigue y dispara al jugador
    """
    
    def __init__(self, id):
        """
        Constructora de la clase:
            - Llama a la constructora de la clase superior ("State")
            - Inicializa "timeInChase" a "0"
        """

        super().__init__(id)
        self.timeInChase = 0
    
    def Start(self, agent):
        """
        Inicia la clase:
            - Inicializa los valores igual que la constructora
        """

        self.timeInChase = 0
    
    def Update(self, perception, map, agent):
        """
        Genera un movimiento y un disparo:
            - Calcula las posiciones del agente y del jugador
            - Si el jugador esta a 5 o menos unidades de distancia, dispara
        Devuelve la tupla (move, shoot)
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

        dist = abs(dx) + abs(dy)
        shot = dist <= 5
        
        self.timeInChase += 1
        
        return (move, shot)
    
    def Transit(self, perception, map):
        """
        Decide la transicion de estado:
            - Si el jugador ya no existe, o el agente a pasado mucho tiempo en "Chase", pasa a "ExecutePlan"
            - Si tiene muy poca vida (<= 2), pasa a "Recover"
            - Si el jugador esta muy cerca (<= 3), pasa a "Attack"
            - Si no, permanece en "Chase"
        """
        
        playerX = perception[AgentConsts.PLAYER_X]
        playerY = perception[AgentConsts.PLAYER_Y]
        agentX = perception[AgentConsts.AGENT_X]
        agentY = perception[AgentConsts.AGENT_Y]

        dist = abs(playerX - agentX) + abs(playerY - agentY)
        
        if (playerX == -1 or playerY == -1) or self.timeInChase > 5 or dist >= 8:
            return "ExecutePlan"
        
        elif dist <= 3:
            return "Attack"
        
        return self.id