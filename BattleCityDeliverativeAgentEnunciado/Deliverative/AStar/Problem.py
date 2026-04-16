class Problem:
    """
    Clase que modela un problema basado en nodos
    """
    
    def __init__(self, initial, goal):
        """
        Constructor de la clase:
            - Inicializa el nodo incial
            - Inicializa el nodo final
        """

        self.initial = initial
        self.goal = goal

    def Initial(self):
        """
        Devuelve el nodo inicial
        """

        return self.initial

    def IsASolution(self, node):
        """
        Devuelve si un nodo es igual al nodo final
        """

        return node == self.goal

    def Heuristic(self, node):
        """
        Calcula la heuristica de un nodo (DEBE SER REIMPLEMENTADO EN OTRA CLASE SUPERIOR)
        """

        raise NotImplementedError("Heuristic no implementado")
        return 0.0

    def GetSuccessors(self, node):
        """
        Calcula los sucesores de un nodo (DEBE SER REIMPLEMENTADO EN UN CLASE SUPERIOR)
        """

        raise NotImplementedError("GetSucessors no implementado")
        return []

    def GetGCostBetween(self, nodeFrom, nodeTo):
        """
        Calcula el coste de ir de un nodo a otro (DEBE SER REIMPLEMENTADO EN UNA CLASE SUPERIOR)
        """

        raise NotImplementedError("GetGCost no implementado")
        return 0.0
    
    def SetGoal(self, goal):
        """
        Establece el objetivo final
        """

        self.goal = goal

    def SetInitial(self, initial):
        """
        Establece el nodo inicial
        """

        self.initial = initial

    def GetGoal(self):
        """
        Devuelve el nodo final
        """

        return self.goal

