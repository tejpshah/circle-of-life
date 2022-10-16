import random 
import collections 
class Graph:
    def __init__(self):
        self.nbrs = {}
        for x in range(1,51):
            self.nbrs[x] = []

    def add_edge(self, v, w):
        self.nbrs[v].append(w)
        self.nbrs[w].append(v)

    def find_nodes_within_radius(self, r, node):
        queue = collections.deque()
        visited = set()
        queue.append((node,0))
        visited.add(node)

        while queue:
            v, d = queue.popleft()
            if d > r:
                break

            yield v, d

            for nbr in self.nbrs[v]:
                if nbr not in visited:
                    visited.add(nbr)
                    queue.append((nbr,d+1))

    def get_random_node(self): return random.choice(list(self.nbrs))

    def add_random_edge(self):
        node = self.get_random_node()
        if len(self.nbrs[node]) >= 3:
            return # node has degree >= 3

        nbrs = [x for x in self.find_nodes_within_radius(5, node)]

        while len(nbrs) > 0:
            n = random.randint(0, len(nbrs)-1)
            n1, d1 = nbrs[n]

            if len(self.nbrs[n1]) < 3:
                self.add_edge(node, n1)
                return  # successfully added edge

            del nbrs[n]  # node already has degree>=3; try another random neighbor

    def print_graph(self):
        for k in sorted(self.nbrs):
            print("%d: %s" % (k, ' '.join([str(x) for x in self.nbrs[k]])))


def main():
    graph = Graph()

    for x in range(1, 51): # make ring structure of nodes 1..50
        graph.add_edge(x, (x % 50) + 1)

    while True: # add random edges until we're done
        graph.add_random_edge()

        if all([len(graph.nbrs[x]) >= 3 for x in graph.nbrs]):
            break;

    graph.print_graph() # display graph structure

    # check if any nodes have degree < 3
    for k in sorted(graph.nbrs):
        if len(graph.nbrs[k]) < 3: print("ERROR: degree of node %d is %d" % (k, len(graph.nbrs[k])))

    print("Number of edges: " + str(sum([len(graph.nbrs[x]) for x in graph.nbrs]) / 2)) # display number of edges



    
if __name__ == '__main__': main()