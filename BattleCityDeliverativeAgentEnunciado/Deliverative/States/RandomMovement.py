from StateMachine.State import State
from States.AgentConsts import AgentConsts
import random

class RandomMovement(State):
    """
    Clase que genera un movimiento aleatorio:
        - Prioriza direcciones libres
        - No elige direcciones peligrosas
    """

    def __init__(self, id):
        """
        Constructora de la clase:
            - Llama al constructor de la clase superior ("State")
            - Inicializa el "timeInRandom" a "0"
            - Inicializa el ultimo movimiento a "None"
        """

        super().__init__(id)
        self.timeInRandom = 0
        self.lastMove = None

    def Start(self, agent):
        """
        Inicia la clase:
            - Inicializa los valores igual que la constructora
        """

        self.timeInRandom = 0
        self.lastMove = None

    def Update(self, perception, map, agent):
        """
        Genera un movimiento aleatorio pero inteligente:
            - Calcula la posicion del agente
            - Calcula la posicion del jugador
            - Por cada direccion posible:
                - Si el agente seguiría en el mapa, en una casilla valida y a mas de "3.0" unidades del jugador
                  lo añade como direccion legal
            - Si la lista de direcciones legales no esta vacia:
                - Elige la anterior (misma direccion) o una aleatoria
            - Si la lista esta vacia, no se mueve
            - Actualiza "timeInRandom" y "lastMove"
        Devuelve una tupla (move, "True")
        """

        agentX = int(perception[AgentConsts.AGENT_X] / 2)
        agentY = int(perception[AgentConsts.AGENT_Y] / 2)
        playerX = perception[AgentConsts.PLAYER_X] / 2
        playerY = perception[AgentConsts.PLAYER_Y] / 2

        legalMoves = []
        directions = [(AgentConsts.MOVE_UP, 0, -1), (AgentConsts.MOVE_DOWN, 0, 1), (AgentConsts.MOVE_RIGHT, 1, 0), (AgentConsts.MOVE_LEFT, -1, 0)]
        for move, dx, dy in directions:
            nx, ny = agentX + dx, agentY + dy
            
            if nx < 0 or nx >= 15 or ny < 0 or ny >= 15:
                continue

            cell = map[nx][ny]
            if cell in (AgentConsts.UNBREAKABLE, AgentConsts.SEMI_UNBREAKABLE):
                continue

            if playerX > 0 and playerY > 0:
                dist = abs(playerX - (agentX + dx)) + abs(playerY - (agentY + dy))
                if dist < 3:
                    continue
            
            legalMoves.append(move)

        if legalMoves:
            if self.lastMove in legalMoves: move = self.lastMove
            else: move = random.choice(legalMoves)
        else: move = AgentConsts.NO_MOVE
        
        self.lastMove = move
        self.timeInRandom += 1

        return move, True

    def Transit(self, perception, map):
        """
        Decide la transicion de estado:
            - Si ha pasado mucho tiempo en "RandomMovement" pasa a "ExecutePlan"
            - Si no se queda en "RandomMovement"
        """

        #self.updateTime += perception[AgentConsts.TIME]
        if self.timeInRandom >= 100:
            return "ExecutePlan"
        
        return self.id
    