from agent import Agent

class Agent1(Agent):
    def __init__(self, location):
        super().__init__(location)

    def move(self, graph, predator, prey):
        # neighbors that are closer to the prey and farther from the predator
        neighbors = graph.get_neighbors(self.location)
        distance_from_prey = dict()
        distance_from_predator = dict()
        for neighbor in neighbors:
            distance_from_prey[neighbor] = self.bfs(graph, neighbor, prey)
            distance_from_predator[neighbor] = self.bfs(graph, neighbor, predator)
        
        shortest_distance_from_prey = min(distance_from_prey.values())
        possible_moves_check_1 = dict()
        for neighbor, distance in distance_from_prey.items():
            if distance == shortest_distance_from_prey:
                possible_moves_check_1[neighbor] = distance_from_predator.get(neighbor)

        if len(possible_moves_check_1) == 1:
            self.location = possible_moves_check_1[0]
            return 1

        # neighbors that are closer to the prey and not closer to the predator
        farthest_distance_from_predator = max(possible_moves_check_1.values())
        possible_moves_check_2 = []
        for neighbor, distance in possible_moves_check_1.items():
            if distance == farthest_distance_from_predator:
                possible_moves_check_2.append(neighbor)

        if len(possible_moves_check_2) == 1:
            self.location = possible_moves_check_2[0]
            return 1

        

        