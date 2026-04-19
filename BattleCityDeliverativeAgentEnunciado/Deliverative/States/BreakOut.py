from StateMachine.State import State
from States.AgentConsts import AgentConsts
from MyProblem.BCProblem import BCProblem
 
class BreakOut(State):
    """
    Clase que genera un escape:
        1. Detecta direccion con menos obstaculos
        2. Intenta avanzar en esa direccion
        3. Si hay un muro, intenta romperlo
        4. Si no puede hacer otra cosa, hace zig-zag
    """
    
    def __init__(self, id):
        """
        Constructor de la clase:
            - LLama a la constructora de la clase superior ("State")
            - Inicializa el contador de zig-zags a "0"
            - Inicializa el "timeInBreakout"
            - Inicializa la direccion de escape a "None"
        """

        super().__init__(id)
        self.timeInBreakout = 0
        self.escapeDirection = None
        self.zigzagCounter = 0
    
    def Start(self, agent):
        """
        Inicia la clase:
            - Inicializa los valores igual que la constructora
        """

        self.timeInBreakout = 0
        self.escapeDirection = None
        self.zigzagCounter = 0
    
    def Update(self, perception, map, agent):
        """
        Genera el mejor movimiento para escapar y/o disparar:
            - Calcula la posicion del agente
            - Por cada direccion posible:
                - Calcula el "coste" de moverse en esa direccion (valor por cada casilla)
                    - Limite del mapa, no destruible, semi no destruible, disparo y jugador tienen valores de "1000"
                    - Casillas destruibles, semi-destruibles tienen valor de "100"
                    - Casillas de vida, vacias, salida y otras tienen valores de "1"
            - Elige la mejor direccion, si esta esta bloqueada elige otra
            - Calcula si necesita disparar o no (muros)
            - Actualiza los contadores
        Devuelve la tupla (move, shoot)
        """
        
        agentX = perception[AgentConsts.AGENT_X]
        agentY = perception[AgentConsts.AGENT_Y]

        costs = {}
        directions = [(AgentConsts.MOVE_UP, 0, -1), (AgentConsts.MOVE_DOWN, 0, 1), (AgentConsts.MOVE_RIGHT, 1, 0), (AgentConsts.MOVE_LEFT, -1, 0)]
        for move, dx, dy in directions:
            nx, ny = agentX + dx, agentY + dy
            
            if nx < 0 or nx >= 15 or ny < 0 or ny >= 15:
                costs[move] = 1000
                continue

            cell = BCProblem.Matrix2VectorCoord(nx, ny, 15)
            match cell:
                case AgentConsts.UNBREAKABLE | AgentConsts.SEMI_UNBREAKABLE | AgentConsts.PLAYER | AgentConsts.SHELL:
                    costs[move] = 1000
                case AgentConsts.BRICK | AgentConsts.SEMI_BREAKABLE:
                    costs[move] = 1000
                case _:
                    costs[move] = 1
        
        if self.escapeDirection is None:
            self.escapeDirection = min(costs, key = costs.get)
        
        if costs[self.escapeDirection] > 500:
            self.escapeDirection = min(costs, key = costs.get)
        
        move = self.escapeDirection
        nextX = agentX + (1 if move == AgentConsts.MOVE_RIGHT else -1 if move == AgentConsts.MOVE_LEFT else 0)
        nextY = agentY + (1 if move == AgentConsts.MOVE_DOWN else -1 if move == AgentConsts.MOVE_UP else 0)
        
        shot = False
        if 0 <= nextX < 15 and 0 <= nextY < 15:
            value = BCProblem.Matrix2VectorCoord(nextX, nextY, 15)
            if value == AgentConsts.BRICK | value == AgentConsts.SEMI_BREAKABLE:
                shot = True
        
        self.timeInBreakout += 1
        self.zigzagCounter += 1
        
        return (move, shot)
    
    def Transit(self, perception, map):
        """
        Decide la transicion del estado:
            - Si el agente no se encuentra bloqueado pasa a "ExecutePlan"
            - Si el agente pasa mucho tiempo escapando, pasa a "ExecutePlan"
            - Si no, se queda en "BreakOut"
        """
        
        agentX = perception[AgentConsts.AGENT_X]
        agentY = perception[AgentConsts.AGENT_Y]
        
        blocked = 0
        for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
            nx, ny = agentX + dx, agentY + dy
            value = BCProblem.Matrix2VectorCoord(nx, ny, 15)
            if nx < 0 or nx >= 15 or ny < 0 or ny >= 15:
                blocked += 1
            elif value in (AgentConsts.UNBREAKABLE, AgentConsts.SEMI_UNBREAKABLE):
                blocked += 1
        
        if blocked < 3 or self.timeInBreakout > 10:
            return "ExecutePlan"
        
        return self.id