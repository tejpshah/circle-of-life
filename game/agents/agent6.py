import random
from copy import deepcopy
from game.predatored import PredatorED
from .agent2 import Agent2


class Agent6(Agent2):
    def __init__(self, location, graph, predator):
        # initialize the location of the agent here
        super().__init__(location)

        # stores the list of all pred prev locations
        self.pred_prev_locations = []

        # we start of the game with knowing where predator is
        self.init_probs_step1(graph, predator)

    def move(self, graph, prey, predator):
        """
        surveys the node with the highest probability of containing the predator
        updates the beliefs
        * if signal is false, update beliefs based on probability that the prey could be in each position
        * if signal is true, beliefs is a one-hot vector
        assume the predator is at one of the locations with the highest probability, chosen randomly
        move according to a modified version of agent2 that accounts for uncertainity 
        """
        signal, surveyed_node = self.survey_node(predator)
        if signal == True:
            self.init_probs_step2(graph, surveyed_node)
        elif signal == False:
            self.init_probs_step3(graph)
        self.normalize_beliefs()
        potential_predator = PredatorED(
            random.choice(self.get_highest_prob_nodes()))

        # MODIFICATION OF A2 CORE LOGIC TO ACCOUNT FOR UNCERTAINTY
        distances = {}
        for nbr in graph.nbrs[self.location]:
            distances[nbr] = self.bfs(graph, nbr, prey.location)
        min_dist = min(distances.values())

        action = 0
        for key, val in distances.items():
            if val == min_dist:
                action = key

        potential_predator_distance = self.bfs(
            graph, self.location, potential_predator.location)

        if potential_predator_distance > 4 or self.beliefs[action] <= 0.1:
            self.location = action
        else:
            distances = {}
            for nbr in graph.nbrs[self.location]:
                distances[nbr] = self.bfs(
                    graph, nbr, potential_predator.location)
            max_dist = max(distances.values())

            action = 0
            for key, val in distances.items():
                if val == max_dist:
                    action = key
            self.location = action

        return None, len(self.pred_prev_locations)

    def move_debug(self, graph, prey, predator):
        """
        debug version of move
        """
        print(f"\nTHE AGENT'S CURRENT LOCATION IS {self.location} ")
        print(f"THE CURRENT FRONTIER IS {self.frontier}")

        signal, surveyed_node = self.survey_node(predator)

        print(f"THE SIGNAL IS {signal} for surveyed node {surveyed_node}")

        print(f"PRIOR BELIEFS: {self.beliefs}")

        if signal == True:
            self.init_probs_step2(graph, surveyed_node)
            print("INIT PROBS 2")
        elif signal == False:
            self.init_probs_step3(graph)
            print("INIT PROBS 3")
        self.normalize_beliefs()
        print(f"THE SUM OF THE PROBABILITIES IS {sum(self.beliefs.values())}")

        print(f"UPDATED BELIEFS: {self.beliefs}")

        potential_predator = PredatorED(
            random.choice(self.get_highest_prob_nodes()))
        print(
            f"WE PREDICT A PREDATOR TO EXIST AT {potential_predator.location}")
        distances = {}
        for nbr in graph.nbrs[self.location]:
            distances[nbr] = self.bfs(graph, nbr, prey.location)
        min_dist = min(distances.values())

        action = 0
        for key, val in distances.items():
            if val == min_dist:
                action = key

        potential_predator_distance = self.bfs(
            graph, self.location, potential_predator.location)

        if potential_predator_distance > 4 or self.beliefs[action] <= 0.1:
            self.location = action
        else:
            distances = {}
            for nbr in graph.nbrs[self.location]:
                distances[nbr] = self.bfs(
                    graph, nbr, potential_predator.location)
            max_dist = max(distances.values())

            action = 0
            for key, val in distances.items():
                if val == max_dist:
                    action = key
            self.location = action

        print(f"The agent's new location is {self.location}")
        return None, len(self.pred_prev_locations)

    def init_probs_step1(self, graph, predator):
        """
        CORE: INITIALIZING INITIAL PROBABILITY

        BELIEF UPDATE STEP 1: 
        P(n_i) = 0 for every node not containing predator 
        P(n_k) = 1 for the kth node containing the predator
        """
        self.beliefs = dict()
        for i in range(1, graph.get_nodes() + 1):
            if i == predator.location:
                self.beliefs[i] = 1
            else:
                self.beliefs[i] = 0
        self.frontier = set()

    def init_probs_step2(self, graph, surveyed_node):
        """
        CORE: SURVEYED NODE CONTAINS PREDATOR!

        Add the location of the predator to the frontier
        Add the location of the predator to our list tracking how many times it was found
        Update the beliefs based on the movement of the optimally moving predator 
        """
        # SETS UP THE CURRENT FRONTIER FOR PROBABILITY MASS REDISTRIBUTION
        self.frontier = set()
        self.frontier.add(surveyed_node)

        self.update_beliefs(graph)

    def init_probs_step3(self, graph):
        """
        CORE: SURVEYED NODE DOES NOT CONTAIN PREDATOR

        Update the beliefs based on the movement of the optimally moving predator 
        """
        self.update_beliefs(graph)

    def update_beliefs(self, graph):
        """
        updates beliefs working under the assumption that the predator will always move optimally
        therefore, predator is guaranteed to be in any one of its neighbors of shortest distance with equal probability
        """
        # print(f"FRONTIER: {self.frontier}")
        counts = self.get_counts_hashmap_neighbor_frontier(graph)
        # print(f"COUNTS: {counts}")
        pruned = self.get_possible_optimal_solutions(counts, graph)
        # print(f"PRUNED: {pruned}")
        self.frontier = set(pruned.keys())

        # WE COMPUTE THE PROBABILITIES BASED ON FREQUENCY
        probability_mass = deepcopy(pruned)
        denominator = sum(probability_mass.values())
        # print(f"PROB MASS: {probability_mass}")

        for key in self.beliefs.keys():
            if key not in probability_mass:
                self.beliefs[key] = 0
            else:
                self.beliefs[key] = probability_mass[key] / denominator

    def survey_node(self, predator):
        """
        RETURNS (SIGNAL=T/F, NODE_SURVEYED=n_i)
        Indicates node surveyed and whether or not prey is there. 
        """
        signal = False
        node = random.choice(self.get_highest_prob_nodes())
        if predator.location == node:
            signal = True
            self.pred_prev_locations.append(node)
        return signal, node

    def get_highest_prob_nodes(self):
        """
        HELPER:
        RETURNS LIST OF ALL NODES OF EQUIVALENT HIGHEST PROBABILITY. 
        """
        PROB, nodes = max(self.beliefs.values()), []
        for node, prob in self.beliefs.items():
            if prob == PROB:
                nodes.append(node)
        return nodes

    def round_belief_probs(self, k=4):
        """
        HELPER:
        UPDATES ALL BELIEFS TO BE ROUNDED TO K DECIMAL PLACES.
        """
        for key in self.beliefs.keys():
            self.beliefs[key] = round(self.beliefs[key], k)

    def normalize_beliefs(self):
        """
        ENSURES THAT ALL PROBABILITIES SUM TO 1
        """
        values_sum = sum(self.beliefs.values())
        for node, probability in self.beliefs.items():
            self.beliefs[node] = probability/values_sum

    def get_counts_hashmap_neighbor_frontier(self, graph):
        """FIND ALL THE COUNTS TO EACH NEIGHBOR IN THE POSSIBLE FRONTIER"""
        counts = dict()
        for node in self.frontier:
            counts[node] = counts.get(node, 0) + 1
            for nbr in graph.nbrs[node]:
                counts[nbr] = counts.get(nbr, 0) + 1
        return counts

    def get_possible_optimal_solutions(self, counts, graph):
        """FIND OUT ALL POSSIBLE OPTIMAL SOLUTIONS THAT CAN BE TAKEN"""
        pruned = {}
        for state in self.frontier:
            d = {}
            min_dist = float("inf")
            d[state] = min(d.get(state, float("inf")),
                           self.bfs(graph, self.location, state))
            for nbr in graph.nbrs[state]:
                d[nbr] = min(d.get(nbr, float("inf")),
                             self.bfs(graph, self.location, nbr))

            min_dist = min(d.values())
            for key in d:
                if d[key] == min_dist:
                    pruned[key] = counts[key]
        return pruned
