
import numpy as np 
class Graph(object):
    def __init__(self, nodes):
        self.nodes = nodes
        self.adjlist = np.zeros((nodes,nodes), dtype = int)
        self.edges = []
        self.primary = []
        self.edgecounter = 0

    def addedgeprim(self, currnode, distance):
        # connect the current node to node "distance" forward in the loop
        self.adjlist[currnode][(currnode + distance) % self.nodes] = 1
        #connect the forward node to the current node in the loop
        self.adjlist[(currnode + distance) % self.nodes][currnode] = 1

        self.edgecounter += 1
        self.primary.append((currnode, (currnode + distance) % self.nodes))

    def countdegree(self, node):
        return sum(self.adjlist[node])

    def pickrandnode(self):
        return random.randint(0,self.nodes - 1)

    def countdegreebelow(self, degree):
        return len([node for node in range(self.nodes) if self.countdegree(node) <= degree])

    def addprimedges(self):
        for i in range(self.nodes):
            self.addedgeprim(i, 1)
            self.addedgeprim(i, 12)

    def addrandedge(self):
        #pick starting node
        start = self.pickrandnode()
        #while the start node has >=3 edges, pick a new random node until it's below 3
        while self.countdegree(start) >= 3:
            start = self.pickrandnode()

        #if there are less than 25 nodes with <3 edges left in the graph
        if self.countdegreebelow(3) >= 25:
            #get the current node's neighbors
            neighbors = [i for i in range(self.nodes) if self.adjlist[start][i] == 1]
            #pick a random neighbor to connect to
            randneighbor = random.choice(neighbors)
            #if statement to make sure the generated edge doesn't already exist, and that it is within the "5-step" distance
            self.adjlist[start][randneighbor] = 1
            #add the edge to the list of edges
            self.edges.append((start, randneighbor))
        else:
            raise ValueError("There are < 25 nodes with degree <3 left.")

    def remove_edge(self, start, end):
        self.adjlist[start][end] = 0
            
class Agent(object): 
    def __init__(self, curr):
        self.curr = curr

    def move(self, graph):
        #Get the neighbors of the current node
        neighbors = [i for i in range(graph.nodes) if graph.adjlist[self.curr][i] == 1]

        #count the number of neighbors
        numneighbors = len(neighbors)

        #choose a random neighbor to move to (excluding option to stay put)
        newloc = random.choice(neighbors)

        #remove the edge between the start and end node of the move
        graph.remove_edge(self.curr, newloc)

        #move to the randomly chosen neighbor
        self.curr = newloc

class Predator(object):
    def __init__(self, curr, target):
        self.curr = curr
        self.target = target

    def move(self, graph):
        #get a list of the agent's neighbors
        neighbors = [i for i in range(graph.nodes) if graph.adjlist[self.curr][i] == 1]

        #find the distances to the agent for each of these neighbors 
        distancetotarget = [abs(i - self.target.curr) % graph.nodes for i in neighbors]

        #get a list of the shortest distances to the agent that were found
        min_distance = min(distancetotarget)

        #create a list of neighbors with the shortest distance to the agent
        mindistneighbors = [neighbors[i] for i in range(len(neighbors)) if distancetotarget[i] == min_distance]

        #choose a random neighbor with the shortest distance to the agent
        newloc = random.choice(mindistneighbors)

        #remove the edge between the start and end node of the move
        graph.remove_edge(self.curr, newloc)

        #move to the randomly chosen neighbor
        self.curr = newloc

class Prey(object):
    def __init__(self, curr):
        self.curr = curr

    def move(self, graph):
        #Get the neighbors of the current node
        neighbors = [i for i in range(graph.nodes) if graph.adjlist[self.curr][i] == 1]

        #count the number of neighbors
        numneighbors = len(neighbors)

        #choose a random neighbor to move to (including option to stay put)
        newloc = random.choice(neighbors + [self.curr])

        #remove the edge between the start and end node of the move
        graph.remove_edge(self.curr, newloc)

        #move to the randomly chosen neighbor
        self.curr = newloc

class Environment(object):
    def __init__(self, agent, prey, predator, graph):
        self.agent = agent
        self.prey = prey
        self.predator = predator
        self.graph = graph

    def playgame(self):
        while self.agent.curr != self.prey.curr and self.agent.curr != self.predator.curr:
            #run the agent's move method
            self.agent.move(self.graph)
            #run the predator's move method
            self.predator.move(self.graph)
            #run the prey's move method
            self.prey.move(self.graph)

        if self.agent.curr == self.prey.curr:
            return True
        else:
            return False

    def trackmoves(self):
        moves_left = []
        moves_right = []

        while self.agent.curr != self.prey.curr and self.agent.curr != self.predator.curr:
            #initialize a list to track the moves that the agent can make
            agent_moves = []
            #get a list of the agent's neighbors
            neighbors = [i for i in range(self.graph.nodes) if self.graph.adjlist[self.agent.curr][i] == 1]
            #for each of the agent's moves, run the Agent class's move method and append it to the list of possible moves and reset back to current position
            for neighbor in neighbors:
                self.agent.move(self.graph)
                agent_moves.append(self.agent.curr)
                self.agent.curr = self.agent.curr - 1
            #get the shortest distance to the prey for each of the agent's possible moves
            distancetotarget = [abs(i - self.prey.curr) % self.graph.nodes for i in agent_moves]
            #find the index of the shortest distance to the prey, move to that node, and append it to the list of moves left/right
            minindex = np.argmin(distancetotarget)
            self.agent.move(self.graph)
            if self.agent.curr > self.prey.curr:
                moves_right.append(self.agent.curr)
            else:
                moves_left.append(self.agent.curr)

        return moves_left, moves_right

    def runtrials(self, numtrials):
        results = []
        for i in range(numtrials):
            results.append(self.playgame())
        return np.mean(results)
a = Agent(0)
p = Prey(25)
pr = Predator(25, a)
nodes = 50
g = Graph(nodes)
env = Environment(a,p,pr,g)
class Track(object):
    def __init__(self, agent, prey, predator, graph):
        self.agent = agent
        self.prey = prey
        self.predator = predator
        self.graph = graph

    def runtrials(self, numtrials):
        #initialize list to track outcomes of trials
        results_left = []
        results_right = []
        #run the trials the specified number of times
        for i in range(numtrials):
            #append the agent's moves left and right of the prey to the results lists
            movesside = self.trackmoves()
            results_left.append(abs(movesside[0][-1] - self.prey.curr))
            results_right.append(abs(movesside[1][-1] - self.prey.curr))

        return results_left, results_right

    def trackmoves(self):
        moves_left = []
        moves_right = []

        while self.agent.curr != self.prey.curr and self.agent.curr != self.predator.curr:
            #initialize a list to track the moves that the agent can make
            agent_moves = []
            #get a list of the agent's neighbors
            neighbors = [i for i in range(self.graph.nodes) if self.graph.adjlist[self.agent.curr][i] == 1]
            #for each of the agent's moves, run the Agent class's move method and append it to the list of possible moves and reset back to current position
            for neighbor in neighbors:
                self.agent.move(self.graph)
                agent_moves.append(self.agent.curr)
                self.agent.curr = self.agent.curr - 1
            #get the shortest distance to the prey for each of the agent's possible moves
            distancetotarget = [abs(i - self.prey.curr) % self.graph.nodes for i in agent_moves]
            #find the index of the shortest distance to the prey, move to that node, and append it to the list of moves left/right
            minindex = np.argmin(distancetotarget)
            self.agent.move(self.graph)
            if self.agent.curr > self.prey.curr:
                moves_right.append(self.agent.curr)
            else:
                moves_left.append(self.agent.curr)

        return moves_left, moves_right

g = Graph(50)
g.addprimedges()
g.addrandedge()
g.addrandedge()

a = Agent(0)
p = Prey(25)
pr = Predator(25, a)
env = Track(a,p,pr,g)
env.runtrials(100)

#change this to different values of 0<=x<=49 to change the locations of the agent, prey, and predator on the graph
a = Agent(25)
p = Prey(1)
pr = Predator(5, a)
env = Environment(a,p,pr,g)


#change this variable to change the number of trials that the graph runs for
numtrials = 100000
results = []
for i in range(numtrials):
    results.append(env.playgame())
np.mean(results)

 