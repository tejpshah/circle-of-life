import random
from .agent1 import Agent1
from game.prey import Prey


class Agent3(Agent1):
    def __init__(self, location, graph):
        super().__init__(location)

        # initialize belief state such that there is equal probability that the prey is in every node except the agent's current one
        self.belief_state = dict()
        for i in range(1, graph.get_nodes() + 1):
            self.belief_state[i] = 1 / \
                (graph.get_nodes() - 1) if i != location else 0

        # stores whether prey was found in the previous step and, if so, where
        self.prey_prev_location = (False, None)

    def get_highest_prob_nodes(self):
        """
        gets nodes that have the highest probability of containing the prey
        """
        highest_prob = max(self.belief_state.values())
        highest_prob_nodes = []
        for node, prob in self.belief_state.items():
            if prob == highest_prob:
                highest_prob_nodes.append(node)

        return highest_prob_nodes

    def move(self, graph, prey, predator):
        # TODO: need to regenerate the belief state based on current status
        # basically, where our current position is 0 and then update the other ones accordingly
        # if agent was last found, update it such that those positions are now 1/3 or 1/4 probability

        # choose node to survey based on the nodes with the highest probability of containing the prey
        survey_node = random.choice(self.get_highest_prob_nodes())
        prey_found = True if prey.location == survey_node else False

        if prey_found:
            # if prey was found, set probability of prey location 1 and everything else to 0
            for i in range(1, graph.get_nodes() + 1):
                self.belief_state[i] = 0 if i != survey_node else 1

            # move according to the rules of agent 1
            super().move(graph, prey.location, predator)

            self.prey_prev_location = (True, prey.location)

            return 1
        else:
            # if prey was not found, update belief state based on derived update rule
            prob_survey_node = self.belief_state[survey_node]
            for node, prob in self.belief_state.items():
                self.belief_state[node] = prob / \
                    (1 - prob_survey_node) if node != survey_node else 0

            # sanity check that the belief state probabilities add up to 1
            assert sum(self.belief_state.values()) == 1

            # select potential prey position and move according to the rules of agent 1
            highest_prob_nodes = self.get_highest_prob_nodes()
            potential_prey = Prey(random.choice(highest_prob_nodes))
            super().move(graph, potential_prey, predator)

            self.prey_prev_location = (False, None)

            return 1

    def move_debug(self, graph, prey, predator):
        return 1
