import heapq

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

        # Cola de prioridad (f(nodo) = g(nodo) + h(nodo))
        heapq.heappush(self.open, (0 + self.problem.Heuristic(self.problem.Initial()), self.problem.Initial()))
        
        # Coste acumulado (g(nodo))
        coste_acumulado = {self.problem.Initial(): 0}

        while(not findGoal and self.open): # Mientras tenga cosas en la cola
            f_nodo, nodo = heapq.heappop(self.open)
            
            if nodo == self.problem.GetGoal():
                findGoal = True
                path = self.ReconstructPath(nodo)
            
            g_actual = coste_acumulado.get(nodo, float('inf'))
            if f_nodo > g_actual + nodo.H():
                continue

            sucesores = self.problem.GetSucessors(nodo)
            for suc in sucesores:
                coste_nuevo = g_actual + suc.G()
                h_nuevo = self.problem.Heuristic(suc)

                if suc not in coste_acumulado or coste_nuevo < coste_acumulado[suc]:
                    coste_acumulado[suc] = coste_nuevo
                    self._ConfigureNode(suc, nodo, suc.G())
                    heapq.heappush(self.open, (coste_nuevo + h_nuevo, suc))

        return path

    #nos permite configurar un nodo (node) con el padre y la nueva G
    def _ConfigureNode(self, node, parent, newG):
        node.SetParent(parent)
        node.SetG(newG)
        #setear la heuristica del nodo
        node.setH(self.problem.Heuristic(node))

    # TODO INUTIL??
    def AppendInOpen(self, node):
        if node.g == None:
            print("AppendInOpen ", node.x, node.y)
        self.open.append(node)

    # TODO INUTIL??
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
        
        nodo_aux = goal
        while nodo_aux is not None:
            path.append(nodo_aux)
            nodo_aux = nodo_aux.GetParent()
        path.reverse()

        return path
