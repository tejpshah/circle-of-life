import random
from copy import deepcopy
from game.predatored import PredatorED
from game.prey import Prey
from .agent8c import Agent8C


class Agent9(Agent8C):
    def __init__(self, location, graph, predator):
        # initialize the location of the agent, graph, predator here
        super().__init__(location, graph, predator)

    def move(self, graph, prey, predator):
        """
        surveys the node with the highest probability of containing the predator if not certain of predator location; otherwise, surveys the nod with the highest probability of containing the prey 
        updates the beliefs
        assume the predator and prey are at one of the locations with the highest probability, chosen randomly
        move according to a modified version of agent2 that accounts for uncertainity 
        """
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
        potential_prey = Prey(random.choice(
            self.get_highest_prob_prey_nodes()))
        potential_pred = PredatorED(random.choice(
            self.get_highest_prob_pred_nodes()))

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
                distances[nbr] = self.bfs(graph, nbr, potential_prey.location)
            min_dist = min(distances.values())

            for key, val in distances.items():
                if val == min_dist:
                    action = key

            potential_predator_distance = self.bfs(
                graph, self.location, potential_pred.location)

            if potential_predator_distance > 3 or self.pred_beliefs[action] <= 0.4 or self.prey_beliefs[action] >= 0.2:
                self.location = action
        return len(self.prev_preys), len(self.prev_preds)

    def get_prey_noisy_survey_belief(self, surveyed_node):
        """
        returns the belief value of the surveyed node, considering that there is a 10% chance it is a false negative 
        P(n_surveyed) = P(signal = False | prey at n_surveyed) * P(prey at n_surveyed) / (P(signal = False | prey at n_surveyed) * P(prey at n_surveyed) + P(signal = False | prey not at n_surveyed) * P(prey not at n_surveyed))
                      = 0.1 * P(prey at n_surveyed) / (0.1 * P(prey at n_surveyed) + 1 * P(prey not at n_surveyed))
                      = (0.1 * 1/48) / (0.1 * 1/48 + 1 * 47/48) = 0.00212314225
        """
        current_belief = self.prey_beliefs[surveyed_node]
        current_antibelief = 1 - current_belief
        new_belief = (0.1 * current_belief) / \
            (0.1 * current_belief + 1 * current_antibelief)

        return new_belief

    def prey_belief_update_1(self, graph, surveyed_node):
        """
        CORE: SURVEYED NODE BUT THE PREY IS NOT THERE AND WE HAVEN'T FOUND PREY BEFORE. 

        BELIEF UPDATE: 
        P(n_i) = 1 / (n-2) for every node not agent's current location or surveyed_node
        P(n_surveyed) = 0.1 * P(prey at n_surveyed) / (0.1 * P(prey at n_surveyed) + 1 * P(prey not at n_surveyed))
        P(n_k) = 0 for the kth node containing the agent
        """
        if self.maybe_noisy_survey == False:
            super().prey_belief_update_1(graph, surveyed_node)
            return 0

        surveyed_node_new_prey_belief = self.get_prey_noisy_survey_belief(
            surveyed_node)

        for node, _ in self.prey_beliefs.items():
            if node == self.location:
                self.prey_beliefs[node] = 0
            elif node == surveyed_node:
                self.prey_beliefs[surveyed_node] = surveyed_node_new_prey_belief
            else:
                self.prey_beliefs[node] = (
                    1 - surveyed_node_new_prey_belief) / (graph.get_nodes() - 2)

    def prey_belief_update_3(self, graph, surveyed_node):
        """
        CORE: SURVEYED NODE DOESN'T CONTAIN PREY BUT WE FOUND A PREY BEFORE!

        BELIEF UPDATE: 
        - Given frontier F_{t-1} at t-1, determine frontier F_{t} at t, and compute # of ways to get to each element in F_{t}
        - Remove the number of ways to get to current agent location if exists in set or current surveyed node if it exists in set
        - Update beliefs based on the number of ways to get to each place in a particular state
        """
        if self.maybe_noisy_survey == False:
            super().prey_belief_update_3(graph, surveyed_node)
            return 0

        counts = dict()
        for node in self.prey_frontier:
            counts[node] = counts.get(node, 0) + 1
            for nbr in graph.nbrs[node]:
                counts[nbr] = counts.get(nbr, 0) + 1
        self.prey_frontier = set(counts.keys())

        probability_mass = deepcopy(counts)
        probability_mass.pop(self.location, None)
        probability_mass.pop(surveyed_node, None)
        denominator = sum(probability_mass.values())

        surveyed_node_new_prey_belief = self.get_prey_noisy_survey_belief(
            surveyed_node)

        for key in probability_mass.keys():
            self.prey_beliefs[key] = probability_mass[key] / \
                denominator * (1 - surveyed_node_new_prey_belief)
        for key in self.prey_beliefs.keys():
            if key not in probability_mass:
                self.prey_beliefs[key] = 0
        self.prey_beliefs[surveyed_node] = surveyed_node_new_prey_belief

    def pred_belief_update_2(self, graph, surveyed_node):
        """
        CORE: SURVEYED NODE DOES NOT CONTAIN PREDATOR

        Update the beliefs based on the movement of the easily distracted predator 
        """
        def get_pred_noisy_survey_belief():
            """
            returns the belief value of the surveyed node, considering that there is a 10% chance it is a false negative 
            P(n_surveyed) = P(signal = False | pred at n_surveyed) * P(pred at n_surveyed) / (P(signal = False | pred at n_surveyed) * P(pred at n_surveyed) + P(signal = False | pred not at n_surveyed) * P(pred not at n_surveyed))
            """
            current_belief = self.pred_beliefs[surveyed_node]
            current_antibelief = 1 - current_belief
            new_belief = (0.1 * current_belief) / \
                ((0.1 * current_belief) + current_antibelief)

            return new_belief

        if self.maybe_noisy_survey == False:
            super().pred_belief_update_2(graph, surveyed_node)
            return 0

        surveyed_node_new_pred_belief = get_pred_noisy_survey_belief()

        self.pred_update_beliefs(graph)

        surveyed_node_new_pred_antibelief = 1 - surveyed_node_new_pred_belief
        surveyed_node_update_beliefs_antibelief = max(1 -
                                                      self.pred_beliefs[surveyed_node], 0.0001)

        for key, value in self.pred_beliefs.items():
            if key == surveyed_node:
                self.pred_beliefs[key] = surveyed_node_new_pred_belief
            else:
                self.pred_beliefs[key] = value * surveyed_node_new_pred_antibelief / \
                    surveyed_node_update_beliefs_antibelief
