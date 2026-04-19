import os
import sys

# Get the directory where this script is located
base_dir = os.path.dirname(os.path.abspath(__file__))

# Add the subdirectories to sys.path using absolute paths
sys.path.insert(0, os.path.join(base_dir, "LGym"))
sys.path.insert(0, os.path.join(base_dir, "Agent"))
sys.path.insert(0, os.path.join(base_dir, "Deliverative"))

from LGym.LGymClient import agentLoop
from Agent.BaseAgent import BaseAgent
from Deliverative.GoalOrientedAgent import GoalOrientedAgent

agent = GoalOrientedAgent("1","Isma")
agentLoop(agent, True)