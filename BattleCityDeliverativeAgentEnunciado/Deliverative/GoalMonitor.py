from States.AgentConsts import AgentConsts

class GoalMonitor:
    """
    Monitor de objetivos que decide el objetivo a seguir y planifica como conseguirlo
    """

    # Valores para los objetivos
    GOAL_COMMAND_CENTRER = 0
    GOAL_LIFE = 1
    GOAL_PLAYER = 2
    GOAL_EXIT = 3
    
    def __init__(self, problem, goals, finalGoal):
        """
        Constructor de la clase:
            - Inicializa la lista de objetivos
            - Inicializa el objetivo final
            - Inicializa el problema
            - Inicializa el contador de "ultimo recalculo"
            - Inicializa el recalculado forzoso a "falso"
        """

        self.goals = goals
        self.finalGoal = finalGoal
        self.problem = problem
        self.lastTime = -1
        self.recalculate = False

    def ForceToRecalculate(self):
        """
        Fuerza el recalculado
        """

        self.recalculate = True

    def NeedReplaning(self, perception, map, agent):
        """
        Metodo que devuelve si necesita replanificar en alguna de las siguientes condiciones:
            - Replanificacion forzosa
            - Ultima replanificacion hace mas de 2 segundos
            - El agente tiene poca vida
            - El jugador esta cerca
            - El "command_center" esta cerca
            - El agente no puede disparar
            - La mejora esta cerca del agente
            - La salida esta cerca del agente
        """

        # Variable de condicion de "replanificacion"
        replaning = False

        # Si el recalculado forzoso esta activo
        replaning = replaning or self.recalculate

        # Si ha pasado mas de 2 segundos sin recalcular
        replaning = replaning or (perception[AgentConsts.TIME] - self.lastTime > 2.0)

        # Si el agente tiene poca vida
        replaning = replaning or (perception[AgentConsts.HEALTH] <= 3)
        
        # Si el jugador esta cerca
        agent_x = perception[AgentConsts.AGENT_X]
        agent_y = perception[AgentConsts.AGENT_Y]
        player_x = perception[AgentConsts.PLAYER_X]
        player_y = perception[AgentConsts.PLAYER_Y]
        replaning = replaning or (abs(player_x - agent_x) + abs(player_y - agent_y) <= 10)

        # Si el command_center esta cerca
        command_center_x = perception[AgentConsts.COMMAND_CENTER_X]
        command_center_y = perception[AgentConsts.COMMAND_CENTER_Y]
        replaning = replaning or (abs(command_center_x - agent_x) + abs(command_center_y - agent_y) <= 10)

        # Si no puede disparar
        replaning = replaning or (not perception[AgentConsts.CAN_FIRE])

        # Si la mejora esta cerca
        life_x = perception[AgentConsts.LIFE_X]
        life_y = perception[AgentConsts.LIFE_Y]
        replaning = replaning or (abs(life_x - agent_x) + abs(life_y - agent_y) <= 10)

        # Si tiene la salida cerca
        exit_x = perception[AgentConsts.EXIT_X]
        exit_y = perception[AgentConsts.EXIT_Y]
        replaning = replaning or (abs(exit_x - agent_x) + abs(exit_y - agent_y) <= 10)

        # Si necesita replanificar por cualquier motivo, acualiza el timer
        if replaning:
            self.lastTime = perception[AgentConsts.TIME]
            self.recalculate = False

        # Devuelve si necesita replanificar o no
        return replaning
    
    def SelectGoal(self, perception, map, agent):
        """
        Selenciona uno de los objetivos en base a la logica:
            - Busca la salida por defecto
            - Si tiene poca vida:
                - Prioriza la curarse
            - Si tiene media vida:
                - Prioriza curarse en caso de que exista y este cerca
                - Si no puede, prioriza al jugador si esta cerca
                - Si no puede, prioriza al "command_center" si esta cerca
                - Si no puede hacer nada de eso, busca la salida
            - Si tiene suficiente vida:
                - Si esta mas cerca el "command_center" lo prioriza
                - Si no, prioriza al jugador
                - Si no puede hacer nada de eso, busca la salida
        Devuelve el nodo (objetivo) selecionado
        """

        # Nodo objetivo por defecto (salida)
        goal_node = self.finalGoal

        # En caso de que tenga poca vida y exista un "objetivo vida", el objetivo es la vida
        vida_actual = perception[AgentConsts.HEALTH]
        if vida_actual <= 3 and self.goals[self.GOAL_LIFE] != None:
            goal_node = self.goals[self.GOAL_LIFE]

        # Objetivos (pueden ser null)
        life_goal = self.goals[self.GOAL_LIFE]
        player_goal = self.goals[self.GOAL_PLAYER]
        command_center_goal = self.goals[self.GOAL_COMMAND_CENTRER]

        # Coordenadas del agente
        agent_x = perception[AgentConsts.AGENT_X]
        agent_y = perception[AgentConsts.AGENT_Y]

        # Distancia a los objetivos (por defecto la maxima)
        dist_life = self.problem.xSize * self.problem.ySize
        dist_play = self.problem.xSize * self.problem.ySize
        dist_comm = self.problem.xSize * self.problem.ySize

        # Si los objetivos existen, recalcula las distancias
        if life_goal != None: dist_life = abs(life_goal.GetX() - agent_x / 2) + abs(life_goal.GetY() - agent_y / 2)
        if player_goal != None: dist_play = abs(player_goal.GetX() - agent_x / 2) + abs(player_goal.GetY() - agent_y / 2)
        if command_center_goal != None: dist_comm = abs(command_center_goal.GetX() - agent_x / 2) + abs(command_center_goal.GetY() - agent_y / 2)

        # En caso de tener suficiente vida
        if vida_actual <= 5:
            # En caso de que exista un "objetivo vida" y "command_center"
            if life_goal != None and command_center_goal != None:
                # En caso de estar mas cerca de la vida prioriza la vida
                if dist_life < dist_comm: goal_node = life_goal
                else: goal_node = command_center_goal
            
            # En caso de que exista un "objetivo vida" y "player"
            elif life_goal != None and player_goal != None:
                # En caso de estar mas cerca de la vida prioriza la vida
                if dist_life < dist_play: goal_node = life_goal
                else: goal_node = player_goal

            # En caso de que exista un "objetivo player" y "command_center"
            elif player_goal != None and command_center_goal != None:
                # En caso de estar mas cerca el jugador prioriza al jugador
                if dist_play < dist_comm: goal_node = player_goal
                else: goal_node = command_center_goal

            # Si ningun objetivo es valido
            else: goal_node = self.finalGoal
        
        if vida_actual > 5:
            # En caso de que exista un "objetivo player" y "command_center"
            if player_goal != None and command_center_goal != None:
                # En caso de estar mas cerca el "command_center" lo prioriza
                if dist_comm < dist_play: goal_node = command_center_goal
                else: goal_node = player_goal

            # Si ningun objetivo es valido
            else: goal_node = self.finalGoal

        return goal_node
    
    def UpdateGoals(self, goal, goalId):
        """
        Actualiza el objetivo en la posicion "id" de la lista de objetivos a "goal"
        """

        self.goals[goalId] = goal
