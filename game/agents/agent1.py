import random
from .agent import Agent


class Agent1(Agent):
    def __init__(self, location):
        super().__init__(location)

        self.current_distance_from_prey = 0
        self.current_distance_from_predator = 0
        self.distance_from_prey = dict()
        self.distance_from_predator = dict()

    def closer_to_prey(self):
        possible_moves = []

        shortest_distance_from_prey = min(self.distance_from_prey.values())
        if not shortest_distance_from_prey < self.current_distance_from_prey:
            return False, possible_moves

        for neighbor, distance in self.distance_from_prey.items():
            if distance == shortest_distance_from_prey:
                possible_moves.append(neighbor)

        return True, possible_moves

    def not_farther_from_prey(self):
        possible_moves = []

        shortest_distance_from_prey = min(self.distance_from_prey.values())
        if not shortest_distance_from_prey <= self.current_distance_from_prey:
            return False, possible_moves

        for neighbor, distance in self.distance_from_prey.items():
            if distance == shortest_distance_from_prey:
                possible_moves.append(neighbor)

        return True, possible_moves

    def farther_from_predator(self, possible_moves):
        filtered_distance_from_predator = dict()
        for neighbor in possible_moves:
            filtered_distance_from_predator[neighbor] = self.distance_from_predator.get(
                neighbor)

        possible_moves = []

        farthest_distance_from_predator = max(
            filtered_distance_from_predator.values())
        if not farthest_distance_from_predator > self.current_distance_from_predator:
            return False, possible_moves

        for neighbor, distance in filtered_distance_from_predator.items():
            if distance == farthest_distance_from_predator:
                possible_moves.append(neighbor)

        return True, possible_moves

    def not_closer_to_predator(self, possible_moves):
        filtered_distance_from_predator = dict()
        for neighbor in possible_moves:
            filtered_distance_from_predator[neighbor] = self.distance_from_predator.get(
                neighbor)

        possible_moves = []

        farthest_distance_from_predator = max(
            filtered_distance_from_predator.values())
        if not farthest_distance_from_predator >= self.current_distance_from_predator:
            return False, possible_moves

        for neighbor, distance in filtered_distance_from_predator.items():
            if distance == farthest_distance_from_predator:
                possible_moves.append(neighbor)

        return True, possible_moves

    def move_condition_1_2(self):
        success, neighbors_closer_to_prey = self.closer_to_prey()
        if not success:
            return False

        success, neighbors_farther_from_predator = self.farther_from_predator(
            neighbors_closer_to_prey)
        if success:
            self.location = random.choice(neighbors_farther_from_predator)
            return True

        success, neighbors_not_closer_to_predator = self.not_closer_to_predator(
            neighbors_closer_to_prey)
        if success:
            self.location = random.choice(neighbors_not_closer_to_predator)
            return True

        return False

    def move_condition_3_4(self):
        success, neighbors_not_farther_from_prey = self.not_farther_from_prey()
        if not success:
            return False

        success, neighbors_farther_from_predator = self.farther_from_predator(
            neighbors_not_farther_from_prey)
        if success:
            self.location = random.choice(neighbors_farther_from_predator)
            return True

        success, neighbors_not_closer_to_predator = self.not_closer_to_predator(
            neighbors_not_farther_from_prey)
        if success:
            self.location = random.choice(neighbors_not_closer_to_predator)
            return True

        return False

    def move_condition_5_6(self):
        success, neighbors_farther_from_predator = self.farther_from_predator(
            self.distance_from_predator.keys())
        if success:
            self.location = random.choice(neighbors_farther_from_predator)
            return True

        success, neighbors_not_closer_to_predator = self.not_closer_to_predator(
            self.distance_from_predator.keys())
        if success:
            self.location = random.choice(neighbors_not_closer_to_predator)
            return True

        return False

    def move(self, graph, prey, predator):
        self.current_distance_from_prey = self.bfs(
            graph, self.location, prey.location)
        self.current_distance_from_predator = self.bfs(
            graph, self.location, predator.location)

        self.distance_from_prey = dict()
        self.distance_from_predator = dict()

        neighbors = graph.get_node_neighbors(self.location)
        for neighbor in neighbors:
            self.distance_from_prey[neighbor] = self.bfs(
                graph, neighbor, prey.location)
            self.distance_from_predator[neighbor] = self.bfs(
                graph, neighbor, predator.location)

        if self.move_condition_1_2():
            return 1
        elif self.move_condition_3_4():
            return 1
        elif self.move_condition_5_6():
            return 1

        return 1

    def move_debug(self, graph, prey, predator):
        self.current_distance_from_prey = self.bfs(graph, self.location, prey.location)
        self.current_distance_from_predator = self.bfs(graph, self.location, predator.location)

        self.distance_from_prey = dict()
        self.distance_from_predator = dict()

        neighbors = graph.get_node_neighbors(self.location)
        for neighbor in neighbors:
            self.distance_from_prey[neighbor] = self.bfs(graph, neighbor, prey.location)
            self.distance_from_predator[neighbor] = self.bfs(graph, neighbor, predator.location)

        print(f"Agent's current location:{self.location}")
        print(f"Predator's current location:{predator.location}")
        print(f"Prey's current location:{prey.location}")
        print(f"Current distance to prey:{self.current_distance_from_prey}")
        print(
            f"Current distance to predator:{self.current_distance_from_predator}")
        print(f"Distance from prey hashmap:{self.distance_from_prey}")
        print(f"Distance from predator hashmap:{self.distance_from_predator}")

        if self.move_condition_1_2():
            return 1
        elif self.move_condition_3_4():
            return 1
        elif self.move_condition_5_6():
            return 1

        return 1
