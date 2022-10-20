import random
import matplotlib.pyplot as plt 
import networkx as nx 

class Graph:
    def __init__(self, nodes=50):
        # initializes number of nodes in the graph
        self.nodes = nodes

        # initializes the graph neighbors list
        self.nbrs = {x: [] for x in range(1, nodes+1)}

        # connects each of the nodes in a large circle
        self.connect_circle()

        # add edges at random to increase connectivity
        self.increase_connectivity()

    def add_edge(self, v, w):
        """adds v to w's neighbor list and vice versa"""
        self.nbrs[v].append(w)
        self.nbrs[w].append(v)

    def connect_circle(self):
        """connects 1 to N nodes in neighbors lists"""
        for i in range(1, self.nodes):
            self.add_edge(i, i+1)
        self.add_edge(1, self.nodes)

    def get_nodes(self):
        """returns number of nodes in graph"""
        return self.nodes

    def get_degree(self, node):
        """returns particular degree of a node"""
        return len(self.nbrs[node])

    def get_neighbors(self):
        """returns neighbors"""
        return self.nbrs

    def get_node_neighbors(self, node):
        """returns neighbors of a node"""
        return self.nbrs[node]

    def candidate_edges_k(self, node, k=5):
        """possible candidates +/- k with degree <3 for edge selection"""
        candidates = set()
        for i in range(node-1, node+k):
            idx = i % self.nodes + 1
            if self.get_degree(idx) < 3:
                candidates.add(idx)
        for i in range(node-k-1, node):
            idx = i % self.nodes + 1
            if self.get_degree(idx) < 3:
                candidates.add(idx)
        if node in candidates:
            candidates.remove(node)

        # removes +1/-1 values of from k if in candidates
        for nbr in self.nbrs[node]:
            if nbr in candidates:
                candidates.remove(nbr)

        return list(candidates)

    def is_graph_done(self):
        """graph is done if each nbr has 3 incoming or no more candidate keys"""
        for i in range(1, self.nodes+1):
            if len(self.nbrs[i]) < 3 and len(self.candidate_edges_k(i)) > 0:
                return False
        return True

    def increase_connectivity(self):
        """
        adds edges to graph by:
        - picking random node with degree less than or equal to 3
        - add edge within 5 steps forwards/backwards in loop
        - do this until no more edges can be added 
        """
        edges_added = 0
        while self.is_graph_done() == False:
            v = random.randint(1, self.nodes)
            while self.get_degree(v) >= 3:
                v = random.randint(1, self.nodes)

            candidate_edges = self.candidate_edges_k(v, k=5)
            if len(candidate_edges) > 0:
                w = random.choice(candidate_edges)
                if w not in self.nbrs[v] and w != v:
                    self.add_edge(v, w)
                    edges_added += 1
        # print(f"The number of edges added is {edges_added}")
    
