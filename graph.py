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
        self.num_added = 0 
        self.nodes = nodes 
        self.adjlist = self.init_adjlist(nodes=nodes)
        #print(self.adjlist)
        self.add_rand_edges() 
        self.visualize_graph()

    def init_adjlist(self, nodes=50):
        hashmap = {i:[(i-1)%(nodes+1), (i+1)%(nodes+1)] for i in range(1, nodes+1)}
        hashmap[1] = [nodes, 2]
        hashmap[50] = [nodes-1, 1]
        return hashmap 

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
            self.num_added += 1
    
    def visualize_graph(self, fn='environment.png'):
        """ Prints out a visualization of the adjacency list
        with the node number as the visual on graph """
        plt.rcParams['figure.figsize'] = [8, 5]
        G = nx.from_dict_of_lists(self.adjlist)
        nx.draw(G, with_labels=True)
        plt.savefig(fn)
        plt.show()


        




g1 = Graph(nodes=50) 
print(g1.adjlist)
print(g1.num_added)