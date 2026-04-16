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

    # TODO revisar si es necesario añadir claves al diccionario de estados
    def __init__(self, id, name):
        """
        Constructor del agente:
            1. Llama a la clase superior (BaseAgent.__init__)
            2. Crea el diccionario de estados
            3. Crea la maquina de estados
            4. Inicializa los atributos del agente a sus valores por defecto
        """

        super().__init__(id, name)
        dictionary = {
            "ExecutePlan" : ExecutePlan("ExecutePlan"),
            "Attack" : Attack("Attack"),
            "RandomMovement" : RandomMovement("RandomMovement")
        }
        
        self.stateMachine = StateMachine("GoalOrientedBehavior", dictionary, "ExecutePlan")
        self.problem = None
        self.aStar = None
        self.plan = None
        self.goalMonitor = None
        self.agentInit = False

    def Start(self):
        """
        Metodo que inicializa la maquina de estado del agente e inicializa sus atributos a sus valores por defecto
        """

        print("Inicio del agente ")
        self.stateMachine.Start(self)
        self.problem = None
        self.aStar = None
        self.plan = None
        self.goalMonitor = None
        self.agentInit = False

    def Update(self, perception, map):
        """
        Funcion que actualiza el estado del agente en base a la percepcion y el mapa:
            - Si "perception" no es del tipo "list", no hace nada y el agente puede disparar
            - Si el agente no ha sido inicializado, fuerza la inicializacion
        Una vez el agente ha sido inicializado:
            1. Actualiza la maquina de estado
            2. Recalcula el objetivo del jugador (nuevo nodo)
            3. Actualiza el Monitor de Objetivos (actualizar el objetivo recalculado)
        Revisa si se necesita replanificar:
            1. Refresca el mapa
            2. Crea un nuevo plan
        Devuelve la accion y si puede disparar
        """

        if perception == True or perception == False:
            return 0, True
        
        if not self.agentInit:
            self.InitAgent(perception, map)
            self.agentInit = True

        action, shot = self.stateMachine.Update(perception, map, self)

        #Actualizar el plan
        goal3Player = self._CreatePlayerGoal(perception)
        self.goalMonitor.UpdateGoals(goal3Player, 2)

        if self.goalMonitor.NeedReplaning(perception, map, self):
            self.problem.InitMap(map) ## refrescamos el mapa
            self.plan = self._CreatePlan(perception, map)

        return action, shot
    
    # TODO revisar porque nos daban una linea comentada
    def _CreatePlan(self, perception, map):
        """
        Crea un plan, siempre y cuando el agente tenga un monitor de objetivos, en funcion de la percepcion y el mapa:
            1. El monitor de objetivos selecciona un objetivo
            2. Establece como nodo inicial para el problema la posicion del agente
            3. Establece el objetivo seleccionado como meta
            4. Devuelve el plan generado por "A*"
        """

        #currentGoal = self.problem.GetGoal()

        if self.goalMonitor != None:
            
            # Elige el objetivo
            selectedGoal = self.goalMonitor.SelectGoal(perception, map, self)

            # Establecemos el nodo incial (actual)
            intialNode = self._CreateInitialNode(perception)
            self.problem.SetInitial(intialNode)

            # Establecer el objetivo seleccionado
            self.problem.SetGoal(selectedGoal)

        # Calcular el plan con A*
        return self.aStar.GetPlan()
        
    @staticmethod
    def CreateNodeByPerception(perception, value, perceptionID_X, perceptionID_Y, ySize):
        """
        Funcion estatica para crear y devuelver un nuevo nodo:
            1. Calcula las coordenadas del "juego" al "mapa"
            2. Crea un nodo sin padre, con "g" y valor, en las coordenadas calculadas
        """

        xMap, yMap = BCProblem.WorldToMapCoord(perception[perceptionID_X], perception[perceptionID_Y], ySize)
        newNode = BCNode(None, BCProblem.GetCost(value), value, xMap, yMap)
        return newNode

    def _CreatePlayerGoal(self, perception):
        """
        Crea y devuelve un nodo para la posicion del jugador
        """

        return GoalOrientedAgent.CreateNodeByPerception(perception, AgentConsts.PLAYER, AgentConsts.PLAYER_X, AgentConsts.PLAYER_Y, 15)

    def _CreateExitGoal(self, perception):
        """
        Crea y devuelve un nodo para la posicion de la salida
        """

        return GoalOrientedAgent.CreateNodeByPerception(perception, AgentConsts.EXIT, AgentConsts.EXIT_X, AgentConsts.EXIT_Y, 15)
    
    def _CreateLifeGoal(self, perception):
        """
        Crea y devuelve un nodo para la posicion de una mejora
        """

        return GoalOrientedAgent.CreateNodeByPerception(perception, AgentConsts.LIFE, AgentConsts.LIFE_X, AgentConsts.LIFE_Y, 15)
    
    def _CreateInitialNode(self, perception):
        """
        Crea y devuelve un nodo en la posicion del agente como "nodo incial", con coste "g" igual a 0
        """

        node = GoalOrientedAgent.CreateNodeByPerception(perception, AgentConsts.NOTHING, AgentConsts.AGENT_X, AgentConsts.AGENT_Y, 15)
        node.SetG(0)
        return node
    
    def _CreateDefaultGoal(self, perception):
        """
        Crea y devuelve un nodo con la posicion de la meta por defecto (command_center)
        """

        return GoalOrientedAgent.CreateNodeByPerception(perception, AgentConsts.COMMAND_CENTER, AgentConsts.COMMAND_CENTER_X, AgentConsts.COMMAND_CENTER_Y, 15)
    
    def InitAgent(self, perception, map):
        """
        Inicializa el agente, no puede hacerse en "start" porque no se tiene conocimiento del mapa o las posiciones:
            1. Crea el problema
            2. Inicializa el mapa
            3. Inicializa A*
            4. Crea los objetivos (nodos) a partir de la percepcion
            5. Crea el monitor de objetivos
            6. Crea un plan inicial
        """

        # Crear el Problema
        self.problem = BCProblem(self._CreateInitialNode(perception), self._CreateDefaultGoal(perception), 15, 15)

        # Inicializar el Mapa
        self.problem.InitMap(map)

        # Inicializar A*
        self.aStar = AStar(self.problem)

        # Crear Objetivos
        goal1CommanCenter = self._CreateDefaultGoal(perception)
        goal2Life = self._CreateLifeGoal(perception)
        goal3Player = self._CreatePlayerGoal(perception)
        exitGoal = self._CreateExitGoal(perception)

        # Crear Monitor de Objetivos
        self.goalMonitor = GoalMonitor(self.problem, [goal1CommanCenter, goal2Life, goal3Player], exitGoal)

        # Crear Plan Inicial
        self.plan = self._CreatePlan(perception, map)

    @staticmethod
    def ShowPlan(plan):
        """
        Metodo estatico que imprime para cada nodo del plan:
            1. Coordenada "x"
            2. Coordenada "y"
            3. Valor del nodo
            5. Coste "g" del nodo
        """

        for n in plan:
            print("X: ",n.x,"Y:",n.y,"[",n.value,"]{",n.G(),"} => ")

    def GetPlan(self):
        """
        Funcion que devuelve el plan a seguir (lista de nodos)
        """

        return self.plan
    
    def End(self, win):
        """
        Metodo que se llama al finalizar el agente, se pasa al estado de terminacion:
            1. Llama a la clase superior (BaseAgent)
            2. Finaliza la maquina de estado
        """

        super().End(win)
        self.stateMachine.End()