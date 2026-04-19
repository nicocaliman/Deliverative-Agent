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
        self.directionToLook = -1
        self.timeInAttack = 0

    def Start(self, agent):
        """
        Inicia la clase:
            - Inicializa los valores igual que la constructora
        """

        self.directionToLook = -1
        self.timeInAttack = 0

    def Update(self, perception, map, agent):
        """
        Genera un movimiento si es necesario y dispara siempre:
            - Calcula la posicion del agente y del jugador
            - Si el jugador se mueve, el agente tambien
        Devuelve la tupla (move, "True")
        """

        playerX = perception[AgentConsts.PLAYER_X] / 2
        playerY = perception[AgentConsts.PLAYER_Y] / 2
        agentX = perception[AgentConsts.AGENT_X] / 2
        agentY = perception[AgentConsts.AGENT_Y] / 2

        dx = playerX - agentX
        dy = playerY - agentY

        if abs(dx) > 1.5: move = AgentConsts.MOVE_RIGHT if dx > 0 else AgentConsts.MOVE_LEFT
        elif abs(dy) > 1.5: move = AgentConsts.MOVE_DOWN if dy > 0 else AgentConsts.MOVE_UP
        else: move = AgentConsts.NO_MOVE
        
        self.timeInAttack += 1
        self.directionToLook = agent.directionToLook
        
        return (move, True)

    def Transit(self,perception, map):
        """
        Decide la transicion de estado:
            - Si el target desaparece (jugador o "command_center"), pasa a "ExecutePlan"
            - Si el jugador se mueve muy lejos, pasa a "Chase"
            - Si el agente tiene poca vida (<= 2), pasa a "Recover"
            - Si no, permanece en "Attack"
        """
        
        playerX = perception[AgentConsts.PLAYER_X]
        playerY = perception[AgentConsts.PLAYER_Y]

        health = perception[AgentConsts.HEALTH]

        agentX = perception[AgentConsts.AGENT_X] / 2
        agentY = perception[AgentConsts.AGENT_Y] / 2

        target = perception[self.directionToLook]
        if target != AgentConsts.PLAYER or target != AgentConsts.COMMAND_CENTER:
            return "ExecutePlan"
        
        playerX /= 2
        playerY /= 2
        dist = abs(playerX - agentX) + abs(playerY - agentY)
        if dist > 5:
            return "Chase"
        
        if health <= 2:
            return "Recover"
        
        return self.id