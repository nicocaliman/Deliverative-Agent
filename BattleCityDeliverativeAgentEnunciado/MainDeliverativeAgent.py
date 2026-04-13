import sys
import os

# Obtener la ruta del directorio donde está el script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Añadir las subcarpetas al sys.path usando rutas absolutas
sys.path.insert(0, os.path.join(script_dir, "LGym"))
sys.path.insert(0, os.path.join(script_dir, "Agent"))
sys.path.insert(0, os.path.join(script_dir, "Deliverative"))

from LGym.LGymClient import agentLoop
from Agent.BaseAgent import BaseAgent
from Deliverative.GoalOrientedAgent import GoalOrientedAgent


agent = GoalOrientedAgent("1","Isma")
agentLoop(agent,True)

 