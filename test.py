from graph import Graph 

### SANITY CHECKING THAT GRAPH WORKS ###
g1 = Graph(nodes=15)
print(g1.nbrs)
g1.visualize_graph()
g1.visualize_graph_circle()