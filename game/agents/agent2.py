import random
from .agent import Agent


class Agent2(Agent):
    def __init__(self, location):
        super().__init__(location)

    def get_optimal_prey_move(self, graph, prey):
        neighbors = graph.get_node_neighbors(prey.location)
        distance_from_agent = dict()
        for neighbor in neighbors:
            distance_from_agent[neighbor] = self.bfs(
                graph, neighbor, self.location)

        maximum_distance_neighbors = max(distance_from_agent.values())
        if maximum_distance_neighbors < self.bfs(graph, prey.location, self.location):
            return prey.location

        potential_max_moves = []
        for neighbor, distance in distance_from_agent.items():
            if distance == maximum_distance_neighbors:
                potential_max_moves.append(neighbor)

        return random.choice(potential_max_moves)

    def get_optimal_predator_move(self, graph, predator):
        neighbors = graph.get_node_neighbors(predator.location)
        distance_from_agent = dict()
        for neighbor in neighbors:
            distance_from_agent[neighbor] = self.bfs(
                graph, neighbor, self.location)

        minimum_distance_neighbors = min(distance_from_agent.values())

        potential_min_moves = []
        for neighbor, distance in distance_from_agent.items():
            if distance == minimum_distance_neighbors:
                potential_min_moves.append(neighbor)

        return random.choice(potential_min_moves)

    def move(self, graph, prey, predator):
        optimal_prey_move = self.get_optimal_prey_move(graph, prey)
        optimal_predator_move = self.get_optimal_predator_move(graph, predator)

        possible_moves = graph.get_node_neighbors(
            self.location) + [self.location]
        move_optimality = dict()
        for move in possible_moves:
            distance_from_prey = self.bfs(graph, move, optimal_prey_move)
            distance_from_predator = self.bfs(
                graph, move, optimal_predator_move)
            move_optimality[move] = distance_from_prey - distance_from_predator

        maximum_move_optimality = max(move_optimality.values())
        potential_max_moves = []
        for move, distance in move_optimality.items():
            if distance == maximum_move_optimality:
                potential_max_moves.append(move)

        self.location = random.choice(potential_max_moves)
        return 1

    def move_debug(self, graph, prey, predator):
        optimal_prey_move = self.get_optimal_prey_move(graph, prey)
        optimal_predator_move = self.get_optimal_predator_move(graph, predator)

        possible_moves = graph.get_node_neighbors(
            self.location) + [self.location]
        move_optimality = dict()
        for move in possible_moves:
            distance_from_prey = self.bfs(graph, move, optimal_prey_move)
            distance_from_predator = self.bfs(
                graph, move, optimal_predator_move)
            move_optimality[move] = distance_from_prey - distance_from_predator

        maximum_move_optimality = max(move_optimality.values())
        potential_max_moves = []
        for move, distance in move_optimality.items():
            if distance == maximum_move_optimality:
                potential_max_moves.append(move)

        self.location = random.choice(potential_max_moves)
        return 1
