import random 
import numpy as np
import networkx as nx  
import matplotlib.pyplot as plt 

class Graph:
    def __init__(self, nodes=50):
        """
        num nodes in graph (n=50)
        adj_list {node# : [n1, n2, ...n_k]}
        undirected edges in adjacency list
        initialize graph for connectivity 
        """
        self.nodes = nodes 
        self.adjlist = {i:[(i+1)%(nodes+1)] for i in range(1, nodes+1)}
        self.adjlist[self.nodes] =  [1] 

    def pick_rand_node(self):
        """picks rand node from (1,nodes)"""
        return random.randint(1, self.nodes)
    
    def count_degree(self, node):
        """counts degree of any node"""
        return len(self.adjlist[node])
    
    def candidate_nodes_k(self, start, k=5):
        """returns list of +/- k candidate nodes"""
        candidates = set()
        for i in range(start-1, start+k):
            candidates.add(i%(self.nodes-1))
        for i in range(start-k, start):
            candidates.add(i%(self.nodes-1))

        solution = set()
        for candidate in candidates:
            solution.add(candidate+1)
        
        if start in solution: 
            solution.remove(start)
        return list(solution)

    def add_edge(self, source, target):
        """adds target to adjlist[source]"""
        if target not in self.adjlist[source]:
            self.adjlist[source].append(target)

    def graph_is_done(self):
        for i in range(1, self.nodes+1):
            if self.count_degree(i) < 3: 
                return False 
        return True 

    def add_rand_edges(self):
        while self.graph_is_done() == False: 
            # pick rand node 
            start = self.pick_rand_node()

            # keep picking rand_node till < 3
            while self.count_degree(start) >= 3:
                start = self.pick_rand_node()

            # add an edge k steps forward/backward
            candidates = self.candidate_nodes_k(start, k=5)
            choice = np.choose(random.randint(0, len(candidates)-1), candidates)
            self.add_edge(start, choice)
    
    def visualize_graph(self, fn='graph.png'):
        """ Prints out a visualization of the adjacency list""" 

        # convert adjacency list to dict
        graph_dict = self.adjlist

        # create a directed graph from dict
        G = nx.DiGraph()
        for key in graph_dict:
            for value in graph_dict[key]:
                if value not in G: 
                    G.add_node(value)
                G.add_edge(key, value)

        # draw graph 
        pos = nx.shell_layout(G)
        nx.draw(G, pos)

        ## save as png 
        plt.savefig(fn, format='PNG')

        




g1 = Graph(nodes=15) 
print(g1.nodes)
print(g1.adjlist)
print(g1.candidate_nodes_k(2, 5))
g1.add_rand_edges()
print(g1.adjlist)
g1.visualize_graph()