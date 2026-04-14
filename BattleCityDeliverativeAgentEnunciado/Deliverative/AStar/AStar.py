
#Algoritmo A* genérico que resuelve cualquier problema descrito usando la plantilla de la
#la calse Problem que tenga como nodos hijos de la clase Node
class AStar:

    def __init__(self, problem):
        self.open = [] # lista de abiertos o frontera de exploración
        self.precessed = set() # set, conjunto de cerrados (más eficiente que una lista)
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
        self.precessed.clear()
        self.open.append(self.problem.Initial())
        path = []
        #mientras no encontremos la meta y haya elementos en open....
        #implementar el bucle de búsqueda del algoritmo A*
        while len(self.open) > 0 and findGoal == False:
            #ordenamos la lista de abiertos por el coste F
            self.open.sort(key=lambda node: node.F())
            #sacamos el nodo con menor coste F
            node = self.open.pop(0)

            #si el nodo es la meta
            if node == self.problem.GetGoal():
                #meta encontrada
                findGoal = True
                #reconstruimos el path
                path = self.ReconstructPath(node)
            else:
                #añadimos el nodo a procesados
                self.precessed.add(node)
                
                #generamos los sucesores
                successors = self.problem.GetSucessors(node)
                #para cada sucesor
                for successor in successors:
                    #si el sucesor no está en procesados
                    if successor not in self.precessed:
                        #si el sucesor no está en abierta
                        if successor not in self.open:
                            #lo añadimos a abierta
                            self.ApendInOpen(successor)
                        else:
                            #si el sucesor está en abierta
                            #comprobamos si el nuevo camino es más eficiente
                            nodeInOpen = self.GetSucesorInOpen(successor)
                            if successor.g < nodeInOpen.g:
                                #si es más eficiente, lo actualizamos
                                self._ConfigureNode(nodeInOpen, node, successor.g)
                           
        return path

    #nos permite configurar un nodo (node) con el padre y la nueva G
    def _ConfigureNode(self, node, parent, newG):
        node.SetParent(parent)
        node.SetG(newG)
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

        currentNode = goal

        while currentNode != None:
            path.append(currentNode)
            currentNode = currentNode.GetParent();
        return path[::-1]



