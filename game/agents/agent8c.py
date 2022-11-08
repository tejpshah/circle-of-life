from copy import deepcopy
from .agent8b import Agent8B


class Agent8C(Agent8B):
    def __init__(self, location, graph, predator):
        # initialize the location of the agent, graph, predator here
        super().__init__(location, graph, predator)

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

        surveyed_node_new_pred_belief = get_pred_noisy_survey_belief()

        self.pred_update_beliefs(graph)

        for key, value in self.pred_beliefs.items():
            if key == surveyed_node:
                self.pred_beliefs[key] = value * \
                    (1 - surveyed_node_new_pred_belief) + \
                    surveyed_node_new_pred_belief
            else:
                self.pred_beliefs[key] = value * \
                    (1 - surveyed_node_new_pred_belief)
