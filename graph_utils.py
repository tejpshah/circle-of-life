import random 

class Graph:
    def __init__(self, nodes=50):
        self.nodes = nodes 
        self.nbrs = {x:[] for x in range(1,nodes+1)}
        self.updates = 0 

        self.connect_circle()
        self.increase_connectivity()

        print(self.nbrs)
    
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
    
    def increase_connectivity(self):
        while True: 
            sims = 1000 
            v = random.randint(1, self.nodes)
            while self.get_degree(v) >= 3: 
                v = random.randint(1, self.nodes)
                if sims == 0: return False 
                sims -= 1
            w = random.choice(self.candidate_edges_k(v, k=5))
            if w not in self.nbrs[v]: 
                self.add_edge(v,w)
                self.updates += 1

        

g1 = Graph(nodes=50)
print(g1.updates)
#print(g1.nbrs)
#print(g1.candidate_edges_k(2, 5))