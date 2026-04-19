from StateMachine.State import State
from States.AgentConsts import AgentConsts
import math
 
class Intercept(State):
    """
    Predice movimiento del jugador e intercepta.
    
    Algoritmo:
    1. Rastrear últimas posiciones del jugador
    2. Calcular vector de velocidad
    3. Predecir posición futura
    4. Mover hacia punto de intercepción
    
    Ventaja sobre Chase: más inteligente, corta caminos
    """
    
    def __init__(self, id):
        """
        Constructora de la clase:
            - Llama al constructor de la clase superior ("State")
            - Inicializa "timeInIntercept" a "0"
            - Inicializa "maxHistory" a "5"
            - Inicializa "playerHistory" a una lista vacia
        """

        super().__init__(id)
        self.playerHistory = []
        self.maxHistory = 5
        self.timeInIntercept = 0
    
    def Start(self, agent):
        """
        Inicia la clase:
            - Inicializa los valores igual que la constructora
        """

        self.playerHistory = []
        self.timeInIntercept = 0
        self.maxHistory = 5
    
    def Update(self, perception, map, agent):
        """
        Genera un movimiento y un disparo para intentar interceptar:
            - Guarda las ultimas 5 posiciones del jugador
            - Calcula la "velocidad" del jugador y su siguiente posicion en 2 frames
            - Si no tiene suficientes datos, usa la posicion actual de referencia
            - Genera un movimiento hacia la posicion calculada
            - Si el jugador esta cerca (<= 4) dispara
        Devuelve la tupla (move, shoot)
        """
        
        playerX = perception[AgentConsts.PLAYER_X] / 2
        playerY = perception[AgentConsts.PLAYER_Y] / 2
        agentX = perception[AgentConsts.AGENT_X] / 2
        agentY = perception[AgentConsts.AGENT_Y] / 2
        
        self.playerHistory.append((playerX, playerY))
        if len(self.playerHistory) > self.maxHistory:
            self.playerHistory.pop(0)
        
        if len(self.playerHistory) >= 3:
            lastX, lastY = self.playerHistory[-1]
            prevX, prevY = self.playerHistory[-2]
            
            velX = lastX - prevX
            velY = lastY - prevY
            
            predictedX = lastX + (velX * 2)
            predictedY = lastY + (velY * 2)
        else:
            predictedX = playerX
            predictedY = playerY
        
        dx = predictedX - agentX
        dy = predictedY - agentY
                
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
        
        dist = abs(playerX - agentX) + abs(playerY - agentY)
        shot = dist >= 3
        
        self.timeInIntercept += 1
        
        return (move, shot)
    
    def Transit(self, perception, map):
        """
        Decide la transicion de estado:
            - Si no existe el jugador, o lleva mucho tiempo en "Intercept", pasa a "ExecutePlan"
            - Si tiene poca vida (<= 3), pasa a "Recover"
            - Si el jugador esta muy cerca, pasa a "Attack"
            - Si no, permanece en "Intercept"
        """
        
        playerX = perception[AgentConsts.PLAYER_X]
        playerY = perception[AgentConsts.PLAYER_Y]
        agentX = perception[AgentConsts.AGENT_X]
        agentY = perception[AgentConsts.AGENT_Y]
        
        dist = abs(playerX - agentX) + abs(playerY - agentY)

        if (playerX == -1 or playerY == -1) or (self.timeInIntercept > 10):
            return "ExecutePlan"

        if dist <= 3:
            return "Attack"
        
        return self.id