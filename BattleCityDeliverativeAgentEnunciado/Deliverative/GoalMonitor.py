import random
from States.AgentConsts import AgentConsts

class GoalMonitor:

    GOAL_COMMAND_CENTRER = 0
    GOAL_LIFE = 1
    GOAL_PLAYER = 2
    GOAL_EXIT = 3

    def __init__(self, problem, goals, finalGoal):
        self.goals = goals
        self.finalGoal = finalGoal
        self.problem = problem
        self.lastTime = -1
        self.recalculate = False

    def ForceToRecalculate(self):
        self.recalculate = True

    def NeedReplaning(self, perception, map, agent):
        currentTime = perception[AgentConsts.TIME]
        
        # Si alguien forzó el recalcular (ej: llegamos al destino anterior)
        if self.recalculate:
            self.recalculate = False
            self.lastTime = currentTime
            return True
            
        # Replanificar cada 1.5 segundos para no perseguir fantasmas
        if self.lastTime == -1 or (currentTime - self.lastTime) > 1.5:
            self.lastTime = currentTime
            return True
            
        # Prioridad máxima: si nuestra salud baja de 40, replanificamos para buscar vida
        if perception[AgentConsts.HEALTH] < 40 and (currentTime - self.lastTime) > 0.3:
            self.lastTime = currentTime
            return True
            
        return False
    
    def SelectGoal(self, perception, map, agent):
        # Estrategia de selección de meta:
        # 1. ¿Poca salud? Ir a por la vida si existe
        if perception[AgentConsts.HEALTH] < 50:
            if self.goals[self.GOAL_LIFE] is not None:
                return self.goals[self.GOAL_LIFE]
                
        # 2. ¿Jugador a la vista? Ir a por él
        if perception[AgentConsts.PLAYER_X] > 0 and perception[AgentConsts.PLAYER_Y] > 0:
            if self.goals[self.GOAL_PLAYER] is not None:
                return self.goals[self.GOAL_PLAYER]
                
        # 3. ¿Base enemiga? Ir a destruirla
        if self.goals[self.GOAL_COMMAND_CENTRER] is not None:
            return self.goals[self.GOAL_COMMAND_CENTRER]
            
        # 4. Caso por defecto: la salida
        return self.finalGoal
    
    def UpdateGoals(self, goal, goalId):
        self.goals[goalId] = goal
