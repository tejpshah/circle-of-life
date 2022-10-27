import random
from .agent2 import Agent2
from game.prey import Prey
from copy import deepcopy


class Agent4(Agent2):
    def __init__(self, location, graph):
        # initializes A3 with given location
        super().__init__(location)

        # intializes belief states to be 1 / (N-1) for probability of prey for every cell that is not the agent
        self.beliefs = dict()
        for i in range(1, graph.get_nodes() + 1):
            self.beliefs[i] = round(
                1 / (graph.get_nodes() - 1), 4) if i != self.location else 0

        # a list that stores the prey's previous locations whenever it is completely known for sure
        self.prey_prev_locations = []

        # keeps track of the nodes that we need in frontier for redistributing probability mass
        self.frontier = set()

        # keeps track of counts and frequencies for redistributing the probability mass
        self.counts = dict()

    def get_highest_prob_nodes(self):
        """gets nodes that have the highest probability of containing the prey"""
        highest_prob = max(self.beliefs.values())
        highest_prob_nodes = []
        for node, prob in self.beliefs.items():
            if prob == highest_prob:
                highest_prob_nodes.append(node)
        return highest_prob_nodes

    def get_signal_prey_exists(self, graph, prey, predator):
        """returns whether or not a prey exists at a location"""
        signal = False

        node_pred_dist = {node: self.bfs(
            graph, node, predator.location) for node in self.get_highest_prob_nodes()}
        highest_pred_dist_nodes = [node for node, dist in node_pred_dist.items(
        ) if dist == max(node_pred_dist.values())]
        node = random.choice(highest_pred_dist_nodes)

        if prey.location == node:
            signal = True
            self.prey_prev_locations.append(node)
        return signal, node

    def update_probs_reinitialize(self, graph, highest_prob_node):
        """reinitialize probabilities according to the limited direction we have on where the prey is"""
        for node, _ in self.beliefs.items():
            if node == self.location or node == highest_prob_node:
                self.beliefs[node] = 0.0
            else:
                self.beliefs[node] = round(1 / (graph.get_nodes() - 2), 4)

    def update_probs_found_prey(self, highest_prob_node):
        """update probabilities according to one hot vector {0,0,0,...,1,....,0}"""
        for node, _ in self.beliefs.items():
            self.beliefs[node] = 0 if node != highest_prob_node else 1
        self.frontier = set()
        self.frontier.add(highest_prob_node)
        self.counts = dict()

    def update_probs_found_prey_distribute_probability(self, graph, highest_prob_node):
        """redistribute probability mass"""
        new_frontier = set()
        for node in self.frontier:
            self.counts[node] = self.counts.get(node, 0) + 1
            new_frontier.add(node)
            for nbr in graph.nbrs[node]:
                self.counts[nbr] = self.counts.get(nbr, 0) + 1
                new_frontier.add(nbr)
        self.frontier = new_frontier

        probability_mass = deepcopy(self.counts)

        self.counts = dict()
        probability_mass[self.location] = 0
        probability_mass[highest_prob_node] = 0

        normalization_denominator = sum(probability_mass.values())
        for key in probability_mass.keys():
            self.beliefs[key] = round(
                probability_mass[key] / normalization_denominator, 4)

    def normalize_beliefs(self):
        values_sum = sum(self.beliefs.values())
        for node, probability in self.beliefs.items():
            self.beliefs[node] = probability/values_sum

    def move(self, graph, prey, predator):
        """
        # take a signal reading of the highest proability node to see if a prey exists 
        # uncertain where prey is at all so reinitialize the belief such that all locations except the surveyed node and our current location are equally probable prey locations
        # we've previously had a signal reading of where the prey actually is 
            # if the current timestep's signal is the prey, update all the proabilities: {0,0,...,1,...,0}
            # otherwise, propogate probability mass of beliefs to neighbors, neighbors of neighbors, and so on (modified bfs)
        """
        signal, highest_prob_node = self.get_signal_prey_exists(
            graph, prey, predator)

        if len(self.prey_prev_locations) == 0:
            """while we do not know where the prey is, update the probabilities of all nodes with Bayes Rule"""
            self.update_probs_reinitialize(graph, highest_prob_node)

        elif signal == True and len(self.prey_prev_locations) > 0:
            """update probabilities according to one hot vector {0,0,0,...,1,....,0}"""
            self.update_probs_found_prey(highest_prob_node)

        elif signal == False and len(self.prey_prev_locations) > 0:
            """redistribute the probability mass based on the number of timesteps since last seen"""
            self.update_probs_found_prey_distribute_probability(
                graph, highest_prob_node)

        self.normalize_beliefs()

        # select potential prey position and move according to the rules of agent 1
        highest_prob_nodes = self.get_highest_prob_nodes()
        potential_prey = Prey(random.choice(highest_prob_nodes))
        super().move(graph, potential_prey, predator)

        return 1

    def move_debug(self, graph, prey, predator):
        """
        debug version
        # take a signal reading of the highest proability node to see if a prey exists 
        # uncertain where prey is at all so reinitialize the belief such that all locations except the surveyed node and our current location are equally probable prey locations
        # we've previously had a signal reading of where the prey actually is 
            # if the current timestep's signal is the prey, update all the proabilities: {0,0,...,1,...,0}
            # otherwise, propogate probability mass of beliefs to neighbors, neighbors of neighbors, and so on (modified bfs)
        """
        signal, highest_prob_node = self.get_signal_prey_exists(
            graph, prey, predator)

        print(f"CURRENT LOCATION {self.location}")
        print(f"SURVEY {highest_prob_node}, SIGNAL = {signal}")

        if len(self.prey_prev_locations) == 0:
            """while we do not know where the prey is, update the probabilities of all nodes with Bayes Rule"""
            self.update_probs_reinitialize(graph, highest_prob_node)
            print(f"REINITIALIZE BELIEFS:\t{self.beliefs}")

        elif signal == True and len(self.prey_prev_locations) > 0:
            """update probabilities according to one hot vector {0,0,0,...,1,....,0}"""
            self.update_probs_found_prey(highest_prob_node)
            print(f"FOUND PREY:\t{self.beliefs}")

        elif signal == False and len(self.prey_prev_locations) > 0:
            """redistribute the probability mass based on the number of timesteps since last seen"""
            self.update_probs_found_prey_distribute_probability(
                graph, highest_prob_node)
            print(f"PROPOGATE PREY BELIEFS:\t{self.beliefs}")

        self.normalize_beliefs()
        print(f'BELIEFS NORMALIZED:\t{self.beliefs}')
        print(f'SUM:\t\t{sum(self.beliefs.values())}\n')

        # select potential prey position and move according to the rules of agent 1
        highest_prob_nodes = self.get_highest_prob_nodes()
        potential_prey = Prey(random.choice(highest_prob_nodes))
        super().move(graph, potential_prey, predator)

        return 1
