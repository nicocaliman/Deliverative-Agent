from StateMachine.State import State
from States.AgentConsts import AgentConsts
import random
 
class Evade(State):
    """
    Clase que evade peligros:
        - Detecta disparos
        - Detecta enemigos cercanos
        - Detecta posiciones vulnerables
    """
    
    def __init__(self, id):
        """
        Constructora de la clase:
            - Llama al constructor de la clase superior ("State")
            - Inicializa "timeInEvade" a "0"
        """

        super().__init__(id)
        self.timeInEvade = 0
    
    def Start(self, agent):
        """
        Inicia la clase:
            - Inicializa los atributos igual que la constructora
        """

        self.timeInEvade = 0
    
    def Update(self, perception, map, agent):
        """
        Genera un movimiento de evasion:
            - Calcula la posicion del agente
            - Si no detecta amenazas, no se mueve
            - Si hay amenazas:
                - Calcula la direccion promedio a la amenaza
                - Busca la mejor direccion y distancia para alejarse
            Devuelve la tupla (bestMove, "False")
        """
        
        agentX = int(perception[AgentConsts.AGENT_X] / 2)
        agentY = int(perception[AgentConsts.AGENT_Y] / 2) 

        threats = self._DetectThreats(perception, map)
        if not threats:
            return (AgentConsts.NO_MOVE, False)
        
        threatX = sum(t[0] for t in threats) / len(threats)
        threatY = sum(t[1] for t in threats) / len(threats)
        
        directions = [(AgentConsts.MOVE_UP, 0, -1), (AgentConsts.MOVE_DOWN, 0, 1), (AgentConsts.MOVE_RIGHT, 1, 0), (AgentConsts.MOVE_LEFT, -1, 0)]
        
        bestMove = AgentConsts.NO_MOVE
        bestDistance = 0
        for move, mdx, mdy in directions:
            newX = agentX + mdx
            newY = agentY + mdy
            
            if self._IsSafe(newX, newY, map):
                dist = abs(newX - threatX) + abs(newY - threatY)
                if dist > bestDistance:
                    bestDistance = dist
                    bestMove = move
        
        self.timeInEvade += 1
        
        return (bestMove, False)
    
    def Transit(self, perception, map):
        """
        Decide la transicion de estado:
            - Si no hay amenazas o lleva mucho tiempo en evade, pasa a "ExecutePlan"
            - Si tiene 3 o menos vida, pasa a "Recover"
            - Si no, sigue en "Evade"
        """
        
        health = perception[AgentConsts.HEALTH]
        
        if not self._DetectThreats(perception, map):
            return "ExecutePlan"
        
        if self.timeInEvade > 200:
            return "ExecutePlan"
        
        if health <= 3:
            return "Recover"
        
        return self.id
    
    def _DetectThreats(self, perception, map):
        """
        Metodo que detecta amenazas en un radio de 5x5 desde el agente:
            - Disparos
            - Enemigos
        Devuelve una lista de posiciones peligrosas
        """

        agentX = int(perception[AgentConsts.AGENT_X] / 2)
        agentY = int(perception[AgentConsts.AGENT_Y] / 2)
        
        threats = []
        for dx in range(-5, 6):
            for dy in range(-5, 6):
                nx, ny = agentX + dx, agentY + dy
                if 0 <= nx < 15 and 0 <= ny < 15:
                    if map[nx][ny] == AgentConsts.SHELL or map[nx][ny] == AgentConsts.PLAYER:
                        threats.append((nx, ny))
        
        return threats
    
    def _IsSafe(self, x, y, map):
        """
        Metodo que devuelve si una posicion es o no segura:
            - Esta dentro del mapa
            - Es "UNBREAKABLE" O "SEMI_UNBREAKABLE"
        """
        
        if x < 0 or x >= 15 or y < 0 or y >= 15:
            return False
        
        cell = map[int(x)][int(y)]
        
        return cell in (AgentConsts.UNBREAKABLE, AgentConsts.SEMI_UNBREAKABLE)