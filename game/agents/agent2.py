from .agent import Agent


class Agent2(Agent):

    def __init__(self, location):
        # initialize agent location
        super().__init__(location)

        # store nbrs dist to prey/pred
        self.nbrs_prey_dist = dict()
        self.nbrs_pred_dist = dict()

    def get_nbrs_min_prey_dist(self):
        """
        retrieves all nbrs of minimal length to prey
        """
        min_dist_to_prey = float("inf")
        for value in self.nbrs_pred_dist.values():
            min_dist_to_prey = min(min_dist_to_prey, value)
        potential_candidates_prey = []
        for key, value in self.nbrs_pred_dist.items():
            if value == min_dist_to_prey:
                potential_candidates_prey.append(key)
        return potential_candidates_prey

    def move(self, graph, prey, predator):
        """
        keep taking the neighbor that that minimizes the distance to the prey 
        if the predator is a distance of 2 edges away, choose the neighbor that maximizes distance away from predator. 
        """
        self.curr_prey_dist = self.bfs(graph, self.location, prey.location)
        self.curr_pred_dist = self.bfs(graph, self.location, predator.location)
        self.nbrs_prey_dist = dict()
        self.nbrs_pred_dist = dict()

        nbrs = graph.get_node_neighbors(self.location)
        for nbr in nbrs:
            self.nbrs_prey_dist[nbr] = self.bfs(graph, nbr, prey.location)
            self.nbrs_pred_dist[nbr] = self.bfs(graph, nbr, predator.location)

        nbrs_min_dist_prey = self.get_nbrs_min_prey_dist()
        if self.curr_pred_dist <= 2 or len(nbrs_min_dist_prey) == 0:
            """move away maximally from nearest predator"""
            max_dist_to_pred = -float("inf")
            for value in self.nbrs_pred_dist.values():
                max_dist_to_pred = max(max_dist_to_pred, value)
            for key, value in self.nbrs_pred_dist.items():
                if value == max_dist_to_pred:
                    self.location = key
                    break
        elif len(nbrs_min_dist_prey) >= 1:
            """choose the candidate option that was given """
            self.location = nbrs_min_dist_prey[0]

        return None, None

    def move_debug(self, graph, prey, predator):
        """
        debug version of move
        """
        self.curr_prey_dist = self.bfs(graph, self.location, prey.location)
        self.curr_pred_dist = self.bfs(graph, self.location, predator.location)
        self.nbrs_prey_dist = dict()
        self.nbrs_pred_dist = dict()

        nbrs = graph.get_node_neighbors(self.location)
        for nbr in nbrs:
            self.nbrs_prey_dist[nbr] = self.bfs(graph, nbr, prey.location)
            self.nbrs_pred_dist[nbr] = self.bfs(graph, nbr, predator.location)

        nbrs_min_dist_prey = self.get_nbrs_min_prey_dist()
        if self.curr_pred_dist <= 2 or len(nbrs_min_dist_prey) == 0:
            """move away maximally from nearest predator"""
            print("move away maximally from nearest predator")
            max_dist_to_pred = -float("inf")
            for value in self.nbrs_pred_dist.values():
                max_dist_to_pred = max(max_dist_to_pred, value)
            for key, value in self.nbrs_pred_dist.items():
                if value == max_dist_to_pred:
                    self.location = key
                    break
        elif len(nbrs_min_dist_prey) >= 1:
            """choose the candidate option that was given"""
            print("choose the candidate option that was given")
            self.location = nbrs_min_dist_prey[0]

        return None, None
