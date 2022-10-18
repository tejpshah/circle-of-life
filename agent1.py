from agent import Agent

class Agent1(Agent):
    def __init__(self, location):
        super().__init__(location)

    def move(self, graph, predator, prey):
        # get a list of the neighbors
        neighbors = graph.get_neighbors(self.location)

        # neighbors that are closer to the prey and farther from the predator
        distance_from_prey = dict()
        distance_from_predator = dict()
        for neighbor in neighbors:
            distance_from_prey[neighbor] = self.bfs(graph, neighbor, prey)
            distance_from_predator[neighbor] = self.bfs(graph, neighbor, predator)
        
        shortest_distance_from_prey = min(distance_from_prey.values())
        possible_moves_check_1_im = dict()
        for neighbor, distance in distance_from_prey.items():
            if distance == shortest_distance_from_prey:
                possible_moves_check_1_im[neighbor] = distance_from_predator.get(neighbor)

        farthest_distance_from_predator = max(possible_moves_check_1_im.values())
        possible_moves_check_1 = []
        for neighbor, distance in possible_moves_check_1_im.items():
            if distance == farthest_distance_from_predator:
                possible_moves_check_1.append(neighbor)

        if len(possible_moves_check_1) == 1:
            self.location = possible_moves_check_1[0]
            return 1

        

        