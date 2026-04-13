
#Algoritmo A* genérico que resuelve cualquier problema descrito usando la plantilla de la
#la clase Problem que tenga como nodos hijos de la clase Node
class AStar:

    def __init__(self, problem):
        self.open = [] # lista de abiertos o frontera de exploración
        self.processed = set() # set, conjunto de cerrados (más eficiente que una lista)
        self.problem = problem #problema a resolver

    def GetPlan(self):
        findGoal = False
        #implementar el algoritmo A*
        #cosas a tener en cuenta:
        #Si el número de sucesores es 0 es que el algoritmo no ha encontrado una solución, devolvemos el path vacio []
        #Hay que invertir el path para darlo en el orden correcto al devolverlo (path[::-1])
        #GetSucesorInOpen(sucesor) nos devolverá None si no lo encuentra, si lo encuentra
        #es que ese sucesor ya está en la frontera de exploración, DEBEMOS MIRAR SI EL NUEVO COSTE ES MENOR QUE EL QUE TENIA ALMACENADO
        #SI esto es asi, hay que cambiarle el padre y setearle el nuevo coste.
        self.open.clear()
        self.processed.clear()
        self.open.append(self.problem.Initial())
        path = []
       
        #mientras no encontremos la meta y haya elementos en open....
        #implementar el bucle de búsqueda del algoritmo A*
        while len(self.open) > 0 and not findGoal:
            #ordenar la lista open por heuristica
            self.open.sort(key=lambda node: node.F())

            #sacamos el primer nodo de la lista open (mejor candidato)
            node = self.open.pop(0)

            #si el nodo es la meta
            if node == self.problem.goal:
                findGoal = True #detengo el bucle
                path = self.ReconstructPath(node) #reconstruyo el path
            else:
                #añadimos el nodo a procesados
                self.processed.add(node)
                #obtenemos los sucesores
                successors = self.problem.GetSucessors(node)
                #para cada sucesor (exploramos los vecinos)
                for successor in successors:
                    #si el sucesor no está en procesados
                    if successor not in self.processed:
                        node_in_open = self.GetSucesorInOpen(successor)

                        if node_in_open == None:
                            self.ApendInOpen(successor)
                        else:
                            new_cost = node.g + self.problem.GetGCost(node_in_open)
                            if new_cost < node_in_open.g:
                                self._ConfigureNode(node_in_open, node, new_cost)
            
        return path

    #nos permite configurar un nodo (node) con el padre y la nueva G
    def _ConfigureNode(self, node, parent, newG):
        node.SetParent(parent)
        node.SetG(newG)
        #Setearle la heuristica que está implementada en el problema. (si ya la tenía será la misma pero por si reutilizais este método para otras cosas)
        node.SetH(self.problem.Heuristic(node))


    def ApendInOpen(self, node):
        if node.g == None:
            print("ApendInOpen ", node.x, node.y)
        self.open.append(node)

    #nos dice si un sucesor está en abierta. Si esta es que ya ha sido expandido y tendrá un coste, comprobar que le nuevo camino no es más eficiente
    #En caso de serlos, _ConfigureNode para setearle el nuevo padre y el nuevo G, asi como su heurística
    def GetSucesorInOpen(self,sucesor):
        i = 0
        found = None
        while found == None and i < len(self.open):
            node = self.open[i]
            i += 1
            if node == sucesor:
                found = node
        return found

    #reconstruye el path desde la meta encontrada.
    def ReconstructPath(self, goal):
        path = []
        #devuelve el path invertido desde la meta hasta que el padre sea None.
        while goal != None:
            path.append(goal)
            goal = goal.parent
        return path[::-1]



