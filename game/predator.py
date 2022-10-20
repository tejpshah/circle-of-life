import random
import queue 

class Predator:
    def __init__(self, location):
        self.location = location

    def bfs(self, graph, source, goal):
        """
        runs BFS on a start to end node and returns the distance to the goal. 
        also stores the previous pointers along the path which can be retrieved to reconstruct the path. 
        """
        #Create queue and enqueue source
        queue = [source]

        #create a dist hashmap to store distance between nodes
        dist = {}
        dist[source] = 0

        #create prev hashmap to maintain a directed shortest path
        prev = {}
        prev[source] = None

        #loop until queue is empty
        while len(queue) > 0:
            node = queue.pop(0)
            nbrs = graph.get_node_neighbors(node)
            for nbr in nbrs:
                if nbr not in dist: 
                    dist[nbr], prev[nbr] = dist[node] + 1, node 
                    if goal == nbr:  
                        return dist[nbr] 

                    queue.append(nbr)
        return -1

    def move(self, graph, agent):
    
        agent_location = agent.location

        # get a list of the predator's neighbors
        neighbors = graph.get_node_neighbors(self.location)

        # calculate distance from each neighbor to agent
        distances = dict()
        for neighbor in neighbors:
            distances[neighbor] = self.bfs(graph, neighbor, agent_location)
        # print(distances)

        # get shortest distance from current location to agent
        shortest_distance = min(distances.values())

        # get all neighbors that result in the shortest path
        potential_moves = []
        for key, value in distances.items():
            if value == shortest_distance:
                potential_moves.append(key)

        # choose neighbor at random
        new_location = random.choice(potential_moves)

        # move to the new location
        self.location = new_location

    def move_debug(self, graph, agent):
        print("\nPredator's Move")

        agent_location = agent.location
        print(f"The agent's current location is: {agent.location}")
        print(f"The predators's current location is: {self.location}")

        # get a list of the predator's neighbors
        neighbors = graph.get_node_neighbors(self.location)
        print(f"The predator's current neighbors are is: {neighbors}")

        # calculate distance from each neighbor to agent
        distances = dict()
        for neighbor in neighbors:
            distances[neighbor] = self.bfs(graph, neighbor, agent_location)
        print(f"The neighbor and corresponding distance to agent is: {distances}")

        # get shortest distance from current location to agent
        shortest_distance = min(distances.values())
        print(f"The shortest distance from predator to the agent is {shortest_distance}")

        # get all neighbors that result in the shortest path
        potential_moves = []
        for key, value in distances.items():
            if value == shortest_distance:
                potential_moves.append(key)
        
        print(f"All the moves with the shortest distances: {potential_moves}")

        # choose neighbor at random
        new_location = random.choice(potential_moves)

        print(f"The predator's new location is randomly selected to be: {new_location}")

        # move to the new location
        self.location = new_location