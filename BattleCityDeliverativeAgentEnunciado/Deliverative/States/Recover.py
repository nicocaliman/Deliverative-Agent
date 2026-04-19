from StateMachine.State import State
from States.AgentConsts import AgentConsts
 
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
        
        lifeX = perception[AgentConsts.LIFE_X] / 2
        lifeY = perception[AgentConsts.LIFE_Y] / 2
        agentX = perception[AgentConsts.AGENT_X] / 2
        agentY = perception[AgentConsts.AGENT_Y] / 2
        
        if lifeX == -1 or lifeY == -1:
            return self._FindShelter(perception, map)
        
        dx = lifeX - agentX
        dy = lifeY - agentY
        if abs(dx) > abs(dy): move = AgentConsts.MOVE_RIGHT if dx > 0 else AgentConsts.MOVE_LEFT
        else: move = AgentConsts.MOVE_DOWN if dy > 0 else AgentConsts.MOVE_UP
        
        self.timeInRecover += 1
        
        return (move, False)
    
    def Transit(self, perception, map):
        """
        Decide la transicion de estado:
            - Si el agente tiene 7 o mas de vida, pasa a "ExecutePlan"
            - Si el agente pasa mucho tiempo en este estado, pasa a "ExecutePlan"
            - Si el jugador esta muy cerca del agente, pasa a "Evade"
            - Si no, sigue en este estado
        """
        
        health = perception[AgentConsts.HEALTH]
        playerX = perception[AgentConsts.PLAYER_X]
        playerY = perception[AgentConsts.PLAYER_Y]
        
        if health >= 7:
            return "ExecutePlan"
        
        if self.timeInRecover > 200:
            return "ExecutePlan"
        
        if playerX > 0 and playerY > 0:
            agentX = perception[AgentConsts.AGENT_X] / 2
            agentY = perception[AgentConsts.AGENT_Y] / 2
            dist = abs(playerX/2 - agentX) + abs(playerY/2 - agentY)
            
            if dist < 5 and health < 5:
                return "Evade"
        
        return self.id
    
    def _FindShelter(self, perception, map):
        """
        Metodo que cuenta cuantos muros adyacentes tiene el agente y decide moverse o no:
            - Cuenta en cada direccion la cantidad de muros
            - Si tiene mas de 2 muros se mueve
            - Si no tiene sufientes, se queda quieto (no puede hacer otra cosa)
        """
        
        agentX = int(perception[AgentConsts.AGENT_X] / 2)
        agentY = int(perception[AgentConsts.AGENT_Y] / 2)
        
        directions = [(AgentConsts.MOVE_UP, 0, -1), (AgentConsts.MOVE_DOWN, 0, 1), (AgentConsts.MOVE_RIGHT, 1, 0), (AgentConsts.MOVE_LEFT, -1, 0)]
        for move, dx, dy in directions:
            nx, ny = agentX + dx, agentY + dy
            
            walls = 0
            for ddx, ddy in [(0,1), (0,-1), (1,0), (-1,0)]:
                nnx, nny = nx + ddx, ny + ddy
                if 0 <= nnx < 15 and 0 <= nny < 15:
                    if map[nnx][nny] in (AgentConsts.BRICK, AgentConsts.UNBREAKABLE, AgentConsts.SEMI_UNBREAKABLE, AgentConsts.SEMI_BREAKABLE):
                        walls += 1
            
            if walls >= 2:
                return (move, False)
        
        return (AgentConsts.NO_MOVE, False)