import random

class Predator:
    def __init__(self, location):
        self.location = location

    def bfs(self, graph, source, goal):
        if source == goal:
            return 0

        queue = [[source]]
        visited = set()

        while queue:
            path = queue.pop(0)
            node = path[-1]
            if node not in visited:
                neighbors = graph.get_neighbors(node)
                for neighbor in neighbors:
                    if neighbor == goal:
                        # print("shortest path: " + str(path + [neighbor]))
                        return len(path) + 1

                    queue.append(list(path) + [neighbor])

            visited.add(node)

        return -1

    def move(self, graph, agent_location):
        # get a list of the predator's neighbors
        neighbors = graph.get_neighbors(self.location)

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
