import heapq

class AStar:
    """
    Algoritmo generico que resuelve cualquier problema descrito por la clase "Problem" que tenga nodos de la clase "Node"
    """

    def __init__(self, problem):
        """
        Constructor de la clase:
            1. Crea una lista de nodos a explorar vacia
            2. Crea un conjunto de nodos ya explorados vacio
            3. Asigna al algoritmo el problema a resolver
        """

        self.open = [] # lista de abiertos o frontera de exploración
        self.processed = set() # set, conjunto de cerrados (más eficiente que una lista)
        self.problem = problem # problema a resolver

    def GetPlan(self):
        """
        Implementacion del algoritmo A*:
            1. Resetea la atributos internos
            2. Calcula los valores del nodo inicial y lo empuja en la lista de prioridad
            3. Crea un diccionario de costes acumulados con clave "nodo", valor "coste acumulado"
        Mientras no haya encontrado la meta y tenga nodos en la lista de exploracion:
            1. Accede al primer elemento de la lista
                1. Si es el nodo objetivo, reconstruye el camino y sale del bucle
                1. Si ya ha sido procesado, salta al siguiente nodo
            2. Añade el nodo a la lista de procesados
            3. Calcula los sucesores del nodo y el coste acumulado
            4. Por cada sucesor hace:
                4. Si ya ha sido procesado, salta al siguiente sucesor
                4. Calcula su nuevo valor de "g"
                4. Si el sucesor no esta en el diccionario de coste acumulado, o el nuevo coste de "g" es menor que el actual:
                    4. 1. Actualiza el diccionario con el nuevo valor
                    4. 2. Calcula los nuevo valores de "h" y "f" del sucesor
                    4. 3. Configura el nodo sucesor
                    4. 4. Añade el nodo sucesor a la lista de exploracion
        Devuelve el camino reconstruido o una lista vacia
        """

        findGoal = False
        self.open.clear()
        self.processed.clear()
        path = []

        # Calculos iniciales
        initial_node = self.problem.Initial()
        initial_h = self.problem.Heuristic(initial_node)
        initial_f = 0 + initial_h

        # Introduce el nodo inicial en la lista de exploración
        heapq.heappush(self.open, (initial_f, id(initial_node), initial_node))

        # Diccionario de costes "g"
        coste_acumulado = {initial_node: 0}

        # Mientra no haya encontrado la meta y tenga cosas en la lista de exploracion
        while(not findGoal and self.open):
            _, _, nodo = heapq.heappop(self.open)

            # Si el nodo actual es igual a la meta, reconstruye el camino y sale del bucle
            if nodo == self.problem.GetGoal():
                findGoal = True
                path = self.ReconstructPath(nodo)
                break
            
            # Si ya ha sido procesado salta ese nodo
            if nodo in self.processed:
                continue
                
            # Añadir a procesados
            self.processed.add(nodo)

            # Calcular sucesores y procesarlos
            g_actual = coste_acumulado[nodo]
            successors = self.problem.GetSuccessors(nodo)
            for succ in successors:
                if succ in self.processed:
                    continue

                # Calcular nuevo coste
                g_nuevo = g_actual + succ.G()

                # Si no se ha explorado o hay un camino mejor
                if succ not in coste_acumulado or g_nuevo < coste_acumulado[succ]:
                    # Añadir el sucesor al diccionario
                    coste_acumulado[succ] = g_nuevo
                    
                    # Calculos del sucesor
                    h_nuevo = self.problem.Heuristic(succ)
                    f_nuevo = g_nuevo + h_nuevo

                    # Configuracion del nodo sucesor
                    self._ConfigureNode(succ, nodo, g_nuevo)

                    # Añadir el sucesor a la lista de exploracion
                    heapq.heappush(self.open, (f_nuevo, id(succ), succ))

        return path

    def _ConfigureNode(self, node, parent, newG):
        """
        Cambia la configuracion de un nodo:
            - Establece su padre
            - Establece el valor de "g"
            - Establece el valor de "h"
        """

        node.SetParent(parent)
        node.SetG(newG)
        node.setH(self.problem.Heuristic(node))

    # TODO revisar si esto es realmente necesario
    def AppendInOpen(self, node):
        """
        Añade un nodo a la lista de nodos a explorar:
            - Si el nodo no tiene valor de "g", muestra por consola sus coordenadas
        """

        if node.g == None:
            print("AppendInOpen ", node.GetX(), node.GetY())
        self.open.append(node)

    # TODO revisar si esto es realmente necesario
    #Si esta es que ya ha sido expandido y tendrá un coste, comprobar que le nuevo camino no es más eficiente
    #En caso de serlos, _ConfigureNode para setearle el nuevo padre y el nuevo G, asi como su heurística
    def GetSuccessorInOpen(self, successor):
        """
        Busca un nodo "successor" en la lista de exploracion de forma lineal:
            - Si lo encuentra devuelve el nodo
            - Si no lo encuentra devuelve "None"
        """

        i = 0
        found = None
        while found == None and i < len(self.open):
            node = self.open[i]
            i += 1
            if node == successor:
                found = node
        
        return found

    def ReconstructPath(self, goal):
        """
        Reconstruye un camino desde el nodo "goal" hasta el padre original:
            - Devuelve una lista de nodos en orden desde el padre hasta "goal"
        """

        path = []
        nodo_aux = goal

        while nodo_aux is not None:
            path.append(nodo_aux)
            nodo_aux = nodo_aux.GetParent()
        
        path.reverse()

        return path