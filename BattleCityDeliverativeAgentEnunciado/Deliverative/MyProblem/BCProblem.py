#import sys
#sys.path.insert(1, '../AStar')
from AStar.Problem import Problem
from MyProblem.BCNode import BCNode
from States.AgentConsts import AgentConsts
import sys
import numpy as np


class BCProblem(Problem):
    

    def __init__(self, initial, goal, xSize, ySize):
        super().__init__(initial, goal)
        self.map = np.zeros((xSize,ySize),dtype=int)
        self.xSize = xSize
        self.ySize = ySize
    
    def InitMap(self,m):
        for i in range(len(m)):
            x,y = BCProblem.Vector2MatrixCoord(i,self.xSize,self.ySize)
            self.map[x][y] = m[i]
    
    #Muestra el mapa por consola
    def ShowMap(self):
        for j in range(self.ySize):
            s = ""
            for i in range(self.xSize):
                s += ("[" + str(i) + "," + str(j) + "," + str(self.map[i][j]) +"]")
            print(s)

    #Calcula la heuristica del nodo en base al problema planteado (Se necesita reimplementar)
    def Heuristic(self, node):
        
        #heurística del nodo        
        dist_Manhattan = abs(node.x - self.goal.x) + abs(node.y - self.goal.y)
        return dist_Manhattan

    #Genera la lista de sucesores del nodo (Se necesita reimplementar)
    def GetSucessors(self, node):
        successors = []
        #sucesores de un nodo dado

        #direccion este
        coord_este = node.x + 1

        #si la coordenada esta dentro del mapa y podemos movernos
        if coord_este >= 0 and coord_este < self.xSize and self.CanMove(self.map[coord_este, node.y]):
            self.CreateNode(successors,node,coord_este,node.y) #creamos el nodo sucesor

        # direccion oeste
        coord_oeste = node.x - 1

        #si la coordenada esta dentro del mapa y podemos movernos
        if coord_oeste >= 0 and coord_oeste < self.xSize and self.CanMove(self.map[coord_oeste, node.y]):
            self.CreateNode(successors,node,coord_oeste,node.y) #creamos el nodo sucesor

        # direccion norte
        coord_norte = node.y + 1

        #si la coordenada esta dentro del mapa y podemos movernos
        if coord_norte >= 0 and coord_norte < self.ySize and self.CanMove(self.map[node.x, coord_norte]):
            self.CreateNode(successors,node,node.x,coord_norte) #creamos el nodo sucesor

        # direccion sur
        coord_sur = node.y - 1

        #si la coordenada esta dentro del mapa y podemos movernos
        if coord_sur >= 0 and coord_sur < self.ySize and self.CanMove(self.map[node.x, coord_sur]):
            self.CreateNode(successors,node,node.x,coord_sur) #creamos el nodo sucesor

        return successors
    
    #métodos estáticos
    #nos dice si podemos movernos hacia una casilla, se debe poner el valor de la casilla como
    #parámetro
    @staticmethod
    def CanMove(value):
        return value != AgentConsts.UNBREAKABLE and value != AgentConsts.SEMI_UNBREKABLE 
    
    #convierte coordenadas mapa en formato vector a matriz
    @staticmethod
    def Vector2MatrixCoord(pos,xSize,ySize):
        x = pos % xSize
        y = pos // ySize #division entera
        return x,y

    #convierte coordenadas mapa en formato matriz a vector
    @staticmethod
    def Matrix2VectorCoord(x,y,xSize):
        return y * xSize + x
    
    #convierte coordenadas del entorno (World) en coordenadas mapa (nótese que la Y está invertida)
    @staticmethod
    def MapToWorldCoord(x,y,ySize):
        xW = x * 2
        yW = (ySize - y - 1) * 2
        return xW, yW
    
    #convierte coordenadas del entorno (World) en coordenadas mapa (nótese que la Y está invertida)
    @staticmethod
    def WorldToMapCoord(xW,yW,ySize):
        x = xW // 2
        y = yW // 2
        y = ySize - y - 1
        return x, y
    
    #versión real del método anterior, que nos ayuda a buscar los centros de las celdas.
    #aqui nos dirá los decimales, es decir como de cerca estamos de la esquina superior derecha
    #un valor de 1.9,1.9 nos dice que estamos en la casilla 1,1 muy cerca de la 2,2
    #en realidad, lo que buscamos es el punto medio de la casilla, es decir la 1.5, 1.5 en el caso
    #de la casilla 1,1
    @staticmethod
    def WorldToMapCoordFloat(xW,yW,ySize):
        x = xW / 2
        invY = (ySize*2) - yW
        invY = invY / 2
        #invY = invY - 1
        return x, invY

    #crea un nodo y lo añade a successors (lista) con el padre indicado y la posición x,y en coordenadas mapa 
    @staticmethod
    def GetCost(value):
        #debes darle un coste a cada tipo de casilla del mapa.
        
        #suelo y objetivos (coste minimo)
        if value == AgentConsts.NOTHING or value == AgentConsts.EXIT or value == AgentConsts.LIFE or value == AgentConsts.PLAYER or value == AgentConsts.COMMAND_CENTER:
            return 1
        #ladrillos y rompibles (coste medio/alto)
        elif value == AgentConsts.BRICK or value == AgentConsts.SEMI_BREKABLE:
            return 10
        #peligro inmediato (balas)
        elif value == AgentConsts.SHELL:
            return 50 #coste muy alto para que el agente evite las balas
        #obstaculos infranqueables
        elif value == AgentConsts.UNBREAKABLE or value == AgentConsts.SEMI_UNBREKABLE:
            return sys.maxsize
        #para cualquier otro valor (other)
        return 1
    
    def CreateNode(self,successors,parent,x,y):
        value=self.map[x][y]
        g=BCProblem.GetCost(value)
        rightNode = BCNode(parent, parent.G() + g, value, x, y)  # coste acumulado desde el inicio
        rightNode.SetH(self.Heuristic(rightNode))
        successors.append(rightNode)

    #Calcula el coste de ir del nodo from al nodo to (Se necesita reimplementar)
    def GetGCost(self, nodeTo):
        return BCProblem.GetCost(nodeTo.value)