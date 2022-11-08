import random
from copy import deepcopy
from .agent7 import Agent7


class Agent7B(Agent7):
    def __init__(self, location, graph, predator):
        # initialize the location of the agent, graph, predator here
        super().__init__(location, graph, predator)

    def survey_node(self, graph, prey, predator):
        """
        RETURNS (PREY SIGNAL=T/F, PREDATOR SIGNAL=T/F, NODE_SURVEYED=n_i)
        Indicates node surveyed and whether or not prey and predator are there. 
        Follows the noisy-survey environment
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
            pred_signal = True if random.uniform(0, 1) <= 0.9 else False
            if pred_signal:
                self.prev_preds.append(node)
        if prey.location == node:
            prey_signal = True if random.uniform(0, 1) <= 0.9 else False
            if prey_signal:
                self.prev_preys.append(node)

        return prey_signal, pred_signal, node

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

        for key in probability_mass.keys():
            self.prey_beliefs[key] = probability_mass[key] / denominator
        for key in self.prey_beliefs.keys():
            if key not in probability_mass:
                self.prey_beliefs[key] = 0

    def normalize_beliefs(self):
        """
        ENSURES THAT ALL PROBABILITIES SUM TO 1
        """
        values_sum = sum(self.pred_beliefs.values())
        for node, probability in self.pred_beliefs.items():
            self.pred_beliefs[node] = probability / max(values_sum, 1)
        values_sum = sum(self.prey_beliefs.values())
        for node, probability in self.prey_beliefs.items():
            self.prey_beliefs[node] = probability / max(values_sum, 1)
