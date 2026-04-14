from Agent.BaseAgent import BaseAgent
from StateMachine.StateMachine import StateMachine
from States.ExecutePlan import ExecutePlan
from GoalMonitor import GoalMonitor
from AStar.AStar import AStar
from MyProblem.BCNode import BCNode
from MyProblem.BCProblem import BCProblem
from States.AgentConsts import AgentConsts
from States.Attack import Attack
from States.RandomMovement import RandomMovement

class GoalOrientedAgent(BaseAgent):

    def __init__(self, id, name):
        super().__init__(id, name)
        dictionary = {
        "ExecutePlan" : ExecutePlan("ExecutePlan"),
        "Attack" : Attack("Attack"),
        "RandomMovement" : RandomMovement("RandomMovement")
        }
        
        self.stateMachine = StateMachine("GoalOrientedBehavior",dictionary,"ExecutePlan")
        self.problem = None
        self.aStar = None
        self.plan = None
        self.goalMonitor = None
        self.agentInit = False
        self.directionToLook = 0

    def Start(self):
        print("Inicio del agente ")
        self.stateMachine.Start(self)
        self.agentInit = False

    def Update(self, perception, map):
        if perception == True or perception == False:
            return 0,True
            
        if not self.agentInit:
            self.InitAgent(perception, map)
            self.agentInit = True

        action, shot = self.stateMachine.Update(perception, map, self)

        # Cada tick actualizamos la ubicación del jugador en el monitor
        goal3Player = self._CreatePlayerGoal(perception)
        self.goalMonitor.UpdateGoals(goal3Player, 2)
        
        # ¿Necesitamos recalcular la ruta?
        if self.goalMonitor.NeedReplaning(perception, map, self):
            self.problem.InitMap(map) 
            self.plan = self._CreatePlan(perception, map)
            
        return action, shot
    
    def _CreatePlan(self, perception, map):
        if self.goalMonitor is not None:
            # 1. Elegimos qué queremos hacer ahora
            targetNode = self.goalMonitor.SelectGoal(perception, map, self)
            # 2. Marcamos nuestra posición actual como inicio
            startNode = self._CreateInitialNode(perception)
            
            # 3. Configuramos el problema para A*
            self.problem.initial = startNode
            self.problem.goal = targetNode
            
            # 4. Buscamos el camino
            print(f"Agente en: {startNode.x}, {startNode.y} | Calculando plan hacia: {targetNode.x}, {targetNode.y}")
            newPlan = self.aStar.GetPlan()
            if newPlan:
                print("Plan encontrado!")
                GoalOrientedAgent.ShowPlan(newPlan)
            else:
                print("No se encontró plan.")
            return newPlan
        return []
        
    @staticmethod
    def CreateNodeByPerception(perception, value, perceptionID_X, perceptionID_Y, ySize):
        xMap, yMap = BCProblem.WorldToMapCoord(perception[perceptionID_X], perception[perceptionID_Y], ySize)
        newNode = BCNode(None, BCProblem.GetCost(value), value, xMap, yMap)
        return newNode

    def _CreatePlayerGoal(self, p):
        return GoalOrientedAgent.CreateNodeByPerception(p, AgentConsts.PLAYER, AgentConsts.PLAYER_X, AgentConsts.PLAYER_Y, 15)

    def _CreateExitGoal(self, p):
        return GoalOrientedAgent.CreateNodeByPerception(p, AgentConsts.EXIT, AgentConsts.EXIT_X, AgentConsts.EXIT_Y, 15)
    
    def _CreateLifeGoal(self, p):
        return GoalOrientedAgent.CreateNodeByPerception(p, AgentConsts.LIFE, AgentConsts.LIFE_X, AgentConsts.LIFE_Y, 15)
    
    def _CreateInitialNode(self, p):
        # El punto de inicio tiene coste G=0
        node = GoalOrientedAgent.CreateNodeByPerception(p, AgentConsts.NOTHING, AgentConsts.AGENT_X, AgentConsts.AGENT_Y, 15)
        node.SetG(0)
        return node
    
    def _CreateDefaultGoal(self, p):
        return GoalOrientedAgent.CreateNodeByPerception(p, AgentConsts.COMMAND_CENTER, AgentConsts.COMMAND_CENTER_X, AgentConsts.COMMAND_CENTER_Y, 15)
    
    def InitAgent(self, perception, map):
        self.problem = BCProblem(None, None, 15, 15)
        self.problem.InitMap(map)
        self.aStar = AStar(self.problem)
        
        # Definimos las metas posibles
        goals = [
            self._CreateDefaultGoal(perception),
            self._CreateLifeGoal(perception),
            self._CreatePlayerGoal(perception)
        ]
        self.goalMonitor = GoalMonitor(self.problem, goals, self._CreateExitGoal(perception))
        
        # Creamos el primer plan
        self.plan = self._CreatePlan(perception, map)

    def GetPlan(self):
        return self.plan

    def End(self, win):
        super().End(win)
        self.stateMachine.End()

    @staticmethod
    def ShowPlan(plan):
        for n in plan:
            print("X: ",n.x,"Y:",n.y,"[",n.value,"]{",n.G(),"} => ")