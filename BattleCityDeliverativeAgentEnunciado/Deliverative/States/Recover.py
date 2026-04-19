from StateMachine.State import State
from States.AgentConsts import AgentConsts
from MyProblem.BCProblem import BCProblem
 
class Recover(State):
    """
    Clase que busca y recoge potenciadores de vida:
        1. Detecta la ubicacion
        2. Se mueve hacia la ubicacion
        3. Si esta muy lejos intenta protegerse
        4. Espera a recuperarase
    """
    
    def __init__(self, id):
        """
        Constructora de la clase:
            - Llama a la constructora de la clase superior ("State")
            - Inicializa "timeInRecover" a 0
            - Inicializa el objetivo de vida a "None"
        """

        super().__init__(id)
        self.timeInRecover = 0
        self.targetLife = None
    
    def Start(self, agent):
        """
        Inicia la clase:
            - Inicializa los atributos igual que la constructura
        """

        self.timeInRecover = 0
        self.targetLife = None
    
    def Update(self, perception, map, agent):
        """
        Genera un movimiento para curarse o defenderse:
            - Calcula las posiciones del agente y de la vida
            - Si no exite vida, busca esconderse
            - Si existe vida, decide hacia donde moverse
        Devuelve la tupla (move, "False")
        """
        
        lifeX = perception[AgentConsts.LIFE_X]
        lifeY = perception[AgentConsts.LIFE_Y]
        agentX = perception[AgentConsts.AGENT_X]
        agentY = perception[AgentConsts.AGENT_Y]
        
        if (lifeX == -1 or lifeY == -1):
            return self._FindShelter(perception, map)
        
        dx = lifeX - agentX
        dy = lifeY - agentY
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
        
        self.timeInRecover += 1
        
        return (move, True)
    
    def Transit(self, perception, map):
        """
        Decide la transicion de estado:
            - Si el agente tiene 7 o mas de vida, pasa a "ExecutePlan"
            - Si el agente pasa mucho tiempo en este estado, pasa a "ExecutePlan"
            - Si el jugador esta muy cerca del agente, pasa a "Evade"
            - Si no, sigue en este estado
        """
        
        health = perception[AgentConsts.HEALTH]
        
        if health >= 3 or self.timeInRecover >= 10:
            return "ExecutePlan"
        
        return self.id
    
    def _FindShelter(self, perception, map):
        """
        Metodo que cuenta cuantos muros adyacentes tiene el agente y decide moverse o no:
            - Cuenta en cada direccion la cantidad de muros
            - Si tiene mas de 2 muros se mueve
            - Si no tiene sufientes, se queda quieto (no puede hacer otra cosa)
        """
        
        agentX = perception[AgentConsts.AGENT_X]
        agentY = perception[AgentConsts.AGENT_Y]
        
        directions = [(AgentConsts.MOVE_UP, 0, -1), (AgentConsts.MOVE_DOWN, 0, 1), (AgentConsts.MOVE_RIGHT, 1, 0), (AgentConsts.MOVE_LEFT, -1, 0)]
        for move, dx, dy in directions:
            nx, ny = agentX + dx, agentY + dy
            walls = 0
            for ddx, ddy in [(0,1), (0,-1), (1,0), (-1,0)]:
                nnx, nny = nx + ddx, ny + ddy
                if 0 <= nnx < 15 and 0 <= nny < 15:
                    value = BCProblem.Matrix2VectorCoord(nnx, nny, 15)
                    if value in (AgentConsts.BRICK, AgentConsts.UNBREAKABLE, AgentConsts.SEMI_UNBREAKABLE, AgentConsts.SEMI_BREAKABLE):
                        walls += 1
            
            if walls >= 2:
                return (move, True)
        
        return (AgentConsts.NO_MOVE, True)