from AStar.Problem import Problem
from MyProblem.BCNode import BCNode
from States.AgentConsts import AgentConsts
import numpy as np
import sys

class BCProblem(Problem):
    """
    Clase basada en "Problem":
        - Tiene un mapa (array bidimensional)
        - Tiene un tamaño "x"
        - Tiene un tamaño "y"
    """
    
    def __init__(self, initial, goal, xSize, ySize):
        """
        Constructor de la clase:
            - Llama al constructor de la clase superior
            - Inicializa el mapa a "0" en cada casilla (tipo "int")
            - Inicializa el tamaño "x"
            - Inicializa el tamaño "y"
        """

        super().__init__(initial, goal)
        self.map = np.zeros((xSize, ySize), dtype = int)
        self.xSize = xSize
        self.ySize = ySize
    
    def InitMap(self, m):
        """
        Inicializa el mapa a partir de un array de valores:
            - Calcula las coordenadas "x" e "y"
            - Asigna a esas coordenas el valor del array en la posicion "i"
        """

        for i in range(len(m)):
            x, y = BCProblem.Vector2MatrixCoord(i, self.xSize, self.ySize)
            self.map[x][y] = m[i]
    
    def ShowMap(self):
        """
        Muestra el mapa por consola
        """

        for j in range(self.ySize):
            s = ""
            for i in range(self.xSize):
                s += ("[" + str(i) + "," + str(j) + "," + str(self.map[i][j]) +"]")
            print(s)

    def Heuristic(self, node):
        """
        Calcula la heuristica de un nodo usando la distancia manhattan:
            - distancia_x = abs(final_x - inicio_x)
            - distancia_y = abs(final_y - inicio_y)
        Devuelve "distancia_x" + "distancia_y"
        """

        dist_x_manhattan = abs(self.GetGoal().GetX() - node.GetX())
        dist_y_manhattan = abs(self.GetGoal().GetY() - node.GetY())

        return dist_x_manhattan + dist_y_manhattan

    def GetSuccessors(self, node):
        """
        Genera los sucesores de un nodo intentado encontrar otro nodo valido:
            - Un nodo es valido si:
                - Esta en una direccion caardinal desde el nodo origen
                - Sus coordenadas estan en los limites del mapa
                - Es un nodo al que se puede llegar
        Devuelve una lista de nodos sucesores
        """

        # Lista de sucesores
        successors = []

        # Lista de movimientos posibles: SUR, NORTE, OESTE, ESTE
        moves = [(0,1), (0,-1), (-1,0), (1,0)]

        # Para cada movimiento posible
        for move in moves:
            new_x = node.GetX() + move[0]
            new_y = node.GetY() + move[1]

            # Si la nueva posicion es valida
            if 0 <= new_x < self.xSize and 0 <= new_y < self.ySize:
                # Si es una posicion a la que se puede mover, lo añade a la lista
                if BCProblem.CanMove(self.map[new_x][new_y]):
                    self.CreateNode(successors, node, new_x, new_y)

        return successors

    @staticmethod
    def CanMove(value):
        """
        Metodo estatico para saber si un nodo es accesible en base al valor de ese nodo
        """

        return value != AgentConsts.UNBREAKABLE and value != AgentConsts.SEMI_UNBREKABLE and value != AgentConsts.SEMI_UNBREKABLE
    
    @staticmethod
    def Vector2MatrixCoord(pos, xSize, ySize):
        """
        Metodo estatico que convierte una posicion del vector de coordenadas a coordenadas del mapa
        """

        x = pos % xSize # modulo 
        y = pos // ySize # division entera
        return x, y

    @staticmethod
    def Matrix2VectorCoord(x, y, xSize):
        """
        Metodo estatico que convierte coordenadas del mapa a una posicion del vector de coordenadas
        """

        return y * xSize + x
    
    @staticmethod
    def MapToWorldCoord(x, y, ySize):
        """
        Metodo estatico que convierte coordenadas del mapa a coordenadas del mundo
        """

        xW = x * 2
        yW = (ySize - y - 1) * 2
        return xW, yW
    
    @staticmethod
    def WorldToMapCoord(xW, yW, ySize):
        """
        Metodo estatico que convierte coordenadas del mundo a coordenadas del mapa
        """

        x = xW // 2
        y = yW // 2
        y = ySize - y - 1
        return x, y
    
    @staticmethod
    def WorldToMapCoordFloat(xW,yW,ySize):
        """
        Metodo estatico que convierte coordenadas del mundo a coordenadas del mapa de tipo "float":
            - Genera coordenadas con decimales en vez de enteras
            - Interesa saber si una coordenada esta cerca del centro de una casilla
        Ejemplo:
            - Una coordenada (1.9, 1.9) representa la casilla (1, 1) cerca de (2, 2)
            - El centro de la casilla es (1.5, 1.5)
        """

        x = xW / 2
        invY = (ySize*2) - yW
        invY = invY / 2
        #invY = invY - 1
        return x, invY

    @staticmethod
    def GetCost(value):
        """
        Metodo estatico que asigna a cada tipo de casilla un coste "g":
            - Casillas accesibles tiene coste "1"
            - Casillas rompibles tienen coste "100"
            - Casillas inrompibles tienen coste "sys.maxsize / 2"
        """
        
        match value:
            # Si la casilla es de tipo: NOTHING, EXIT, JUGADOR, COMMAND_CENTER, LIFE u OTHER
            case AgentConsts.NOTHING | AgentConsts.EXIT | AgentConsts.PLAYER | AgentConsts.COMMAND_CENTER | AgentConsts.LIFE | AgentConsts.OTHER:
                return 1
            # Si la casilla es de tipo: BRICK o SEMI_BREAKABLE
            case AgentConsts.BRICK | AgentConsts.SEMI_BREAKABLE:
                return 100
            # Cualquier otro caso
            case _:
                return sys.maxsize / 2

        # Caso extremo (no deberia llegar)
        return sys.maxsize
    
    def CreateNode(self, successors, parent, x, y):
        """
        Crea un nodo y lo añade a una lista de sucesores:
            - El valor del nodo es el valor del mapa en las coordenadas "x" e "y"
            - El valor "g" del nodo se calcula en funcion del tipo de casilla
            - El valor "h" del nodo lo calcula la clase
        """

        value = self.map[x][y]
        g = BCProblem.GetCost(value)
        rightNode = BCNode(parent, g, value, x, y)
        rightNode.SetH(self.Heuristic(rightNode))
        successors.append(rightNode)

    def GetGCost(self, nodeTo):
        """
        Devuelve el coste "g" de ir del nodo incial al recibido por parametro:
        """

        return BCProblem.GetCost(nodeTo.GetValue())