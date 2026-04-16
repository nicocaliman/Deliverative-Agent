from AStar.Node import Node

class BCNode(Node):
    """
    Clase basada en "Node":
        - Tiene un valor
        - Tiene una coordenada "x"
        - Tiene una coordenada "y"
    """

    def __init__(self, parent, g, value, x, y):
        """
        Constructor de la clase:
            - Llama al constructor de la clase superior
            - Inicializa el valor del nodo
            - Inicializa la coordenada "x"
            - Inicializa la coordenada "y"
        """

        super().__init__(parent, g)
        self.value = value
        self.x = int(x)
        self.y = int(y)
    
    def __repr__(self):
        """
        Devuelve la representacion del nodo:
            - "BCNode(x, y)"
        """

        return f"BCNode(x = {self.x}, y = {self.y})"

    def __eq__(self, other):
        """
        Compara dos nodos en base a sus coordenadas, son iguales si:
            - Las coordenadas "x" coinciden
            - Las coordenadas "y" coinciden
        """

        if other == None:
            return False
        
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        """
        Calcula el hash del nodo:
            - hash(tuple(x, y))
        """

        return hash((self.x, self.y))
    
    def GetX(self):
        """
        Devuelve la coordenada "x" del nodo
        """

        return self.x
    
    def GetY(self):
        """
        Devuelve la coordenada "y" del nodo
        """

        return self.y

    def GetValue(self):
        """
        Devuelve el valor del nodo
        """
        
        return self.value
    
