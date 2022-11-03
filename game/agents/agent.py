"""
SANITY CHECKED: AGENT SHOULD BE WORKING AS SPECIFIED PER ASSIGNMENT DESCRIPTION.
"""

from abc import ABC, abstractmethod


class Agent(ABC):
    def __init__(self, location):
        self.location = location

    def bfs(self, graph, source, goal):
        """
        standard implementation of BFS from source to goal distances 
        """
        # create queue and enqueue source
        queue = [source]

        # create a dist hashmap to store distance between nodes
        dist = {}
        dist[source] = 0

        # create prev hashmap to maintain a directed shortest path
        prev = {}
        prev[source] = None

        # loop until queue is empty
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

    @abstractmethod
    def move(self, graph, prey, predator):
        pass

    @abstractmethod
    def move_debug(self, graph, prey, predator):
        pass
