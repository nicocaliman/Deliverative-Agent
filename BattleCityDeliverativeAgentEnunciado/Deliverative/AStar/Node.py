
class Node:
    """
    Clase que modela un nodo de un grafo:
        - Tiene un padre (puede ser "None")
        - Tiene un coste "g"
        - Tiene una heuristica "h"
    """

    def __init__(self, parent, g):
        """
        Constructor de la clase, inicializa los atributos "parent", "g" y "h":
            - "h" se inicializa a 0.0
        """

        self.parent = parent
        self.g = g
        self.h = 0.0

    def GetParent(self):
        """
        Devuelve el padre del nodo
        """

        return self.parent
    
    def __repr__(self):
        """
        Representacion de la clase (NO HACE NADA)
        """

        pass

    def __eq__(self, other):
        """
        Compara dos nodos (NO HACE NADA)
        """

        raise NotImplementedError("__eq__ debe ser reimplementado en la clase hija")
        pass

    def __hash__(self):
        """
        Calcula el hash del nodo (NO HACE NADA)
        """

        pass
    
    def SetParent(self, p):
        """
        Establece el padre de un nodo
        """

        self.parent = p

    def F(self):
        """
        Calcula el coste total de un nodo:
            - "F" = "g" + "h"
        """

        return self.g + self.h
    
    def SetG(self, g):
        """
        Establece el coste "g" del nodo:
            - "g" es el coste de llegar desde otro nodo (inicial) hasta este
        """

        self.g = g

    def SetH(self, h):
        """
        Establece el valor de "h" del nodo:
            - "h" lo calcula la clase "Problem"
        """

        self.h = h
    
    def G(self):
        """
        Devuelve el valor de "g"
        """

        return self.g
    
    def H(self):
        """
        Devuelve el valor de "h"
        """

        return self.h
    
    def toString(self):
        """
        Devuelve la representacion del nodo en "string"
        """

        return str(self.__repr__())