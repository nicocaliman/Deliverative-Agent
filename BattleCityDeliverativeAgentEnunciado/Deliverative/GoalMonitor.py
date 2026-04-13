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
        if self.recalculate:
            self.recalculate = False
            self.lastTime = perception[AgentConsts.TIME]
            return True
        #definir la estrategia de cuando queremos recalcular        
        #puede ser , por ejemplo cada cierto tiempo o cuando tenemos poca vida.

        if self.lastTime == -1:
            self.lastTime = perception[AgentConsts.TIME]
            return True
        if perception[AgentConsts.TIME] - self.lastTime > 2:
            self.lastTime = perception[AgentConsts.TIME]
            return True

        #replanificar por salud (cada 0.5s)
        if perception[AgentConsts.HEALTH] < 50 and (perception[AgentConsts.TIME] - self.lastTime > 0.5):
            self.lastTime = perception[AgentConsts.TIME]
            return True
        return False
    
    #selecciona la meta mas adecuada al estado actual
    def SelectGoal(self, perception, map, agent):
        #definir la estrategia del cambio de meta
        #si la vida del tanque es menor a 50, vamos a por la vida
        if perception[AgentConsts.HEALTH] < 50:
            if self.goals[self.GOAL_LIFE] is not None:
                return self.goals[GoalMonitor.GOAL_LIFE]
        #si el jugador esta vivo, vamos a por el
        if perception[AgentConsts.PLAYER_X] >= 0 and perception[AgentConsts.PLAYER_Y] >= 0:
           if self.goals[self.GOAL_PLAYER] is not None:
            return self.goals[GoalMonitor.GOAL_PLAYER]
        #por defecto, vamos a por la base
        if self.goals[self.GOAL_COMMAND_CENTRER] is not None:
            return self.goals[GoalMonitor.GOAL_COMMAND_CENTRER]
        #si todo falla, la meta final (salida)
        return self.finalGoal
    
    def UpdateGoals(self,goal, goalId):
        self.goals[goalId] = goal
