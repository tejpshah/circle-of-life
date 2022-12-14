import random
from copy import deepcopy
from game.predatored import PredatorED
from game.prey import Prey
from .agent2 import Agent2


class Agent10(Agent2):
    def __init__(self, location, graph, predator):
        # initialize the location of the agent here
        super().__init__(location)

        # stores the list of all pred and prey prev locations
        self.prev_preds = []
        self.prev_preys = []

        # stores prey and pred belief prob distribution
        self.prey_beliefs = dict()
        self.pred_beliefs = dict()

        # initializes original prob distribution
        self.init_belief_probs_1(graph, predator)

        self.pred_frontier = set()
        self.pred_frontier.add(predator.location)
        self.prey_frontier = set()

    def move(self, graph, prey, predator):
        """
        surveys the node with the highest probability of containing the predator if not certain of predator location; otherwise, surveys the nod with the highest probability of containing the prey 
        updates the beliefs
        assume the predator and prey are at one of the locations with the highest probability, chosen randomly
        move according to a modified version of agent2 that accounts for uncertainity 
        """

        # if we have >=30% belief of where the predator is at any 1 location, we move and distribute the probability mass
        if max(self.pred_beliefs.values()) > 0.05:
            pred_node = random.choice(self.get_highest_prob_pred_nodes())
            prey_node = random.choice(self.get_highest_prob_prey_nodes())

            # propogate pred probability mass
            self.pred_belief_update_2(graph, pred_node)

            # propogate prey probability mass
            if len(self.prev_preys) == 0:
                self.prey_belief_update_1(graph, prey_node)
            else:
                self.prey_belief_update_3(graph, prey_node)

            self.normalize_beliefs()

            potential_prey = Prey(prey_node)
            potential_pred = PredatorED(pred_node)

            # MODIFICATION OF A2 CORE LOGIC TO ACCOUNT FOR UNCERTAINTY
            distances = {}
            for nbr in graph.nbrs[self.location]:
                distances[nbr] = self.bfs(graph, nbr, potential_pred.location)
            max_dist = max(distances.values())

            action = 0
            for key, val in distances.items():
                if val == max_dist:
                    action = key

            # WE ARE MORE CERTAIN ABOUT PREDATOR LOCATION
            if len(self.prev_preys) == 0:
                self.location = action
            # WE KEEP RUNNING AWAY MAXIMALLY FROM PREDATOR UNTIL WE KNOW WHERE PREY IS
            else:
                distances = {}
                for nbr in graph.nbrs[self.location]:
                    distances[nbr] = self.bfs(
                        graph, nbr, potential_prey.location)
                min_dist = min(distances.values())

                for key, val in distances.items():
                    if val == min_dist:
                        action = key

                potential_predator_distance = self.bfs(
                    graph, self.location, potential_pred.location)

                if potential_predator_distance > 3 or self.pred_beliefs[action] <= 0.4 or self.prey_beliefs[action] >= 0.2:
                    self.location = action

        # otherwise, we survey the node and and try to get a better measurement of where the predator is and update the beliefs
        else:
            prey_signal, pred_signal, surveyed_node = self.survey_node(
                graph, prey, predator)

            if len(self.prev_preys) == 0:
                self.prey_belief_update_1(graph, surveyed_node)
            elif prey_signal == True and len(self.prev_preys) > 0:
                self.prey_belief_update_2(surveyed_node)
            elif prey_signal == False and len(self.prev_preys) > 0:
                self.prey_belief_update_3(graph, surveyed_node)

            if pred_signal == True:
                self.pred_belief_update_1(graph, surveyed_node)
            elif pred_signal == False:
                self.pred_belief_update_2(graph, surveyed_node)

            self.normalize_beliefs()
        return len(self.prev_preys), len(self.prev_preds)

    def move_debug(self, graph, prey, predator):
        """
        debug version of move
        """
        prey_signal, pred_signal, surveyed_node = self.survey_node(
            graph, prey, predator)
        print(
            f"\nWE SURVEYED NODE: {surveyed_node}\t Prey Signal: {prey_signal} \t Pred Signal: {pred_signal}\n")

        print(f"\nTHE PREY BELIEFS ARE BEFORE: {self.prey_beliefs}\n")
        print(f"\nTHE PRED BELIEFS ARE BEFORE: {self.pred_beliefs}\n")

        if len(self.prev_preys) == 0:
            print("PREY BELIEF UPDATE: 1/48 Everywhere")
            self.prey_belief_update_1(graph, surveyed_node)
        elif prey_signal == True and len(self.prev_preys) > 0:
            print("PREY BELIEF UPDATE: FOUND PREY!")
            self.prey_belief_update_2(surveyed_node)
        elif prey_signal == False and len(self.prev_preys) > 0:
            print("PREY BELIEF UPDATE: DISTRIBUTE PROBS MASS")
            self.prey_belief_update_3(graph, surveyed_node)

        if pred_signal == True:
            print("PRED BELIEF UPDATE: FOUND PREY")
            self.pred_belief_update_1(graph, surveyed_node)
        elif pred_signal == False:
            print("PRED BELIEF UPDATE: DISTRIBUTE PROBS MASS")
            self.pred_belief_update_2(graph, surveyed_node)
        self.normalize_beliefs()

        print(f"\nTHE PREY BELIEFS ARE NOW: {self.prey_beliefs}\n")
        print(f"\nTHE PRED BELIEFS ARE NOW: {self.pred_beliefs}\n")

        potential_prey = Prey(random.choice(
            self.get_highest_prob_prey_nodes()))
        potential_pred = PredatorED(random.choice(
            self.get_highest_prob_pred_nodes()))

        print(f"\nTHE ACTUAL AGENT IS AT {self.location}")
        print(f"THE POTENTIAL PREY IS AT {potential_prey.location}")
        print(f"THE POTENTIAL PRED IS AT {potential_pred.location}")
        print(f"THE ACTUAL PREY IS AT {prey.location}")
        print(f"THE ACTUAL PRED IS AT {predator.location}\n")

        super().move(graph, potential_prey, potential_pred)

        print(f"THE AGENT NOW MOVES TO {self.location}")

        return len(self.prev_preys), len(self.prev_preds)

    def init_belief_probs_1(self, graph, predator):
        """
        CORE: INITIALIZING INITIAL PROBABILITY FOR BOTH PREY AND PREDATOR
        """
        for i in range(1, graph.get_nodes() + 1):
            if i == self.location:
                self.prey_beliefs[i] = 0
            else:
                self.prey_beliefs[i] = 1 / (graph.get_nodes() - 1)
        for i in range(1, graph.get_nodes() + 1):
            if i == predator.location:
                self.pred_beliefs[i] = 1
            else:
                self.pred_beliefs[i] = 0

    def survey_node(self, graph, prey, predator):
        """
        RETURNS (PREY SIGNAL=T/F, PREDATOR SIGNAL=T/F, NODE_SURVEYED=n_i)
        Indicates node surveyed and whether or not prey and predator are there. 
        """
        prey_signal, pred_signal, node = False, False, 0

        boolean_set = {self.pred_beliefs[i] for i in range(
            1, graph.get_nodes()+1) if self.pred_beliefs[i] == 1}
        is_certain_where_pred_is = len(boolean_set) == 1

        #print(f"THE BOOLEAN SET IS: {boolean_set} \t is_certain_where_pred_is={is_certain_where_pred_is}")

        if not is_certain_where_pred_is:
            #print("WE ARE NOT CERTAIN WHERE PREDATOR IS SO WE SURVEY WRT A5!")
            highest_prob_pred_nodes = self.get_highest_prob_pred_nodes()
            node = random.choice(highest_prob_pred_nodes)
        elif is_certain_where_pred_is:
            #print("WE ARE CERTAIN WHERE PREDATOR IS AND NOT PREY SO WE SURVEY WRT A3")
            highest_prob_prey_nodes = self.get_highest_prob_prey_nodes()
            node = random.choice(highest_prob_prey_nodes)

        if predator.location == node:
            pred_signal = True
            self.prev_preds.append(node)
        if prey.location == node:
            prey_signal = True
            self.prev_preys.append(node)

        return prey_signal, pred_signal, node

    def prey_belief_update_1(self, graph, surveyed_node):
        """
        CORE: SURVEYED NODE BUT THE PREY IS NOT THERE AND WE HAVEN'T FOUND PREY BEFORE. 

        BELIEF UPDATE: 
        P(n_i) = 1 / (n-2) for every node not agent's current location or surveyed_node
        P(n_k) = P(n_surveyed) = 0 for the kth node containing the agent and the surveyed node
        """
        for node, _ in self.prey_beliefs.items():
            if node == self.location or node == surveyed_node:
                self.prey_beliefs[node] = 0
            else:
                self.prey_beliefs[node] = 1 / (graph.get_nodes() - 2)

    def prey_belief_update_2(self, surveyed_node):
        """
        CORE: SURVEYED NODE CONTAINS PREY!

        BELIEF UPDATE: 
        P(n_surveyed) = 1
        P(n_i) = 0 for all i != n_surveyed
        """
        for node, _ in self.prey_beliefs.items():
            if node == surveyed_node:
                self.prey_beliefs[node] = 1
            else:
                self.prey_beliefs[node] = 0
        self.prey_frontier = set()
        self.prey_frontier.add(surveyed_node)

    def prey_belief_update_3(self, graph, surveyed_node):
        """
        CORE: SURVEYED NODE DOESN'T CONTAIN PREY BUT WE FOUND A PREY BEFORE!

        BELIEF UPDATE: 
        - Given frontier F_{t-1} at t-1, determine frontier F_{t} at t, and compute # of ways to get to each element in F_{t}
        - Remove the number of ways to get to current agent location if exists in set or current surveyed node if it exists in set
        - Update beliefs based on the number of ways to get to each place in a particular state
        """
        counts = dict()
        for node in self.prey_frontier:
            counts[node] = counts.get(node, 0) + 1
            for nbr in graph.nbrs[node]:
                counts[nbr] = counts.get(nbr, 0) + 1
        self.prey_frontier = set(counts.keys())

        probability_mass = deepcopy(counts)
        probability_mass[self.location] = 0
        probability_mass[surveyed_node] = 0
        denominator = sum(probability_mass.values())

        for key in probability_mass.keys():
            self.prey_beliefs[key] = probability_mass[key] / denominator
        for key in self.prey_beliefs.keys():
            if key not in probability_mass:
                self.prey_beliefs[key] = 0

    def pred_update_beliefs(self, graph):
        """
        updates beliefs working under the assumption that the predator will always move optimally
        therefore, predator is guaranteed to be in any one of its neighbors of shortest distance with equal probability
        """
        def get_countshashmap_neighbor_frontier():
            counts = dict()
            for node in self.pred_frontier:
                counts[node] = counts.get(node, 0) + 1
                for nbr in graph.nbrs[node]:
                    counts[nbr] = counts.get(nbr, 0) + 1
            return counts

        def get_possible_optimal_solutions(counts):
            pruned = {}
            for state in self.pred_frontier:
                d = {}
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

        # print(self.pred_frontier)
        counts = get_countshashmap_neighbor_frontier()
        # print(counts)
        pruned = get_possible_optimal_solutions(counts)
        # print(pruned)
        self.pred_frontier = set(pruned.keys())
        # print(self.pred_frontier)

        probability_mass = deepcopy(pruned)
        # print(probability_mass)
        denominator = sum(probability_mass.values())

        for key in self.pred_beliefs.keys():
            if key not in probability_mass:
                self.pred_beliefs[key] = 0
            else:
                self.pred_beliefs[key] = probability_mass[key] / denominator

    def pred_belief_update_1(self, graph, surveyed_node):
        """
        CORE: SURVEYED NODE CONTAINS PREDATOR!

        Add the location of the predator to the frontier
        Add the location of the predator to our list tracking how many times it was found
        Update the beliefs based on the movement of the easily distracted predator 
        """
        self.pred_frontier = set()
        self.pred_frontier.add(surveyed_node)

        self.pred_update_beliefs(graph)

    def pred_belief_update_2(self, graph, surveyed_node):
        """
        CORE: SURVEYED NODE DOES NOT CONTAIN PREDATOR

        Update the beliefs based on the movement of the easily distracted predator 
        """
        self.pred_update_beliefs(graph)

    def get_highest_prob_pred_nodes(self):
        """
        HELPER:
        RETURNS LIST OF ALL NODES OF EQUIVALENT HIGHEST PROBABILITY OF CONTAINING PRED. 
        """
        PROB, nodes = max(self.pred_beliefs.values()), []
        for node, prob in self.pred_beliefs.items():
            if prob == PROB:
                nodes.append(node)
        return nodes

    def get_highest_prob_prey_nodes(self):
        """
        HELPER:
        RETURNS LIST OF ALL NODES OF EQUIVALENT HIGHEST PROBABILITY OF CONTAINING PREY. 
        """
        PROB, nodes = max(self.prey_beliefs.values()), []
        for node, prob in self.prey_beliefs.items():
            if prob == PROB:
                nodes.append(node)
        return nodes

    def normalize_beliefs(self):
        """
        ENSURES THAT ALL PROBABILITIES SUM TO 1
        """
        values_sum = sum(self.pred_beliefs.values())
        for node, probability in self.pred_beliefs.items():
            self.pred_beliefs[node] = probability / max(values_sum, 1)
        values_sum = sum(self.prey_beliefs.values())
        for node, probability in self.prey_beliefs.items():
            self.prey_beliefs[node] = probability/values_sum
