from abc import ABC, abstractmethod


class Agent(ABC):
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
                neighbors = graph.get_node_neighbors(node)
                for neighbor in neighbors:
                    if neighbor == goal:
                        # print("shortest path: " + str(path + [neighbor]))
                        return len(path) + 1

                    queue.append(list(path) + [neighbor])

            visited.add(node)

        return -1

    @abstractmethod
    def move(self, graph, prey, predator):
        pass
