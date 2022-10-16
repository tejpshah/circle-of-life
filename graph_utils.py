import random 

class Graph:
    def __init__(self, nodes=50):
        self.nodes = nodes 
        self.nbrs = {x:[] for x in range(1,nodes+1)}
        self.connect_circle()

    def add_edge(self, v, w):
        self.nbrs[v].append(w) 
        self.nbrs[w].append(v) 
    
    def connect_circle(self):
        for i in range(1, self.nodes): 
            self.add_edge(i, i+1)
        self.add_edge(1, self.nodes)

    def get_degree(self, node):
        return len(self.nbrs[node])
    
    def candidate_edges_k(self, node, k=5):
        candidates = set()
        for i in range(node-1, node+k):
            candidates.add(i%self.nodes+1)
        for i in range(node-k-1, node):
            candidates.add(i%self.nodes+1)
        if node in candidates: candidates.remove(node)
        return list(candidates)
    
    def is_graph_done(self):
        for nbr in self.nbrs.keys():
            if self.get_degree(nbr) < 3:
                return False 
        return True 

    def increase_connectivity(self):
        steps = 0 
        while self.is_graph_done() or steps <= 25: 
            v = random.randint(1, self.nodes)

            timeout = 1000 
            while self.get_degree(v) >= 3 and timeout > 0: 
                v = random.randint(1, self.nodes)
                timeout -= 1 

            candidate_edges = self.candidate_edges_k(self.nodes, k=5)
            w = random.choice(candidate_edges)
            timeout = 1000 
            while self.get_degree(w) >= 3 and w not in self.nbrs[w] and timeout > 0: 
                w = random.choice(candidate_edges)
                timeout -= 1
            
            if timeout == 0: break 
            
            if w != v: 
                self.add_edge(v,w)
                steps += 1 
        print(steps)

g1 = Graph(nodes=50)
print(g1.nbrs)
g1.increase_connectivity()
print(g1.nbrs)
