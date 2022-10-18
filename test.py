from graph import Graph 
from prey import Prey
from predator import Predator

### SANITY CHECKING THAT GRAPH WORKS ###
g1 = Graph(nodes=10)
print(g1.nbrs)
g1.visualize_graph()
g1.visualize_graph_circle()

"""
prey = Prey(2)
prey.move(g1)
prey.move(g1)

predator = Predator(2)
predator.move(g1, 5)
"""