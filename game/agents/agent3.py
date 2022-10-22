import random
from .agent1 import Agent1
from game.prey import Prey

class Agent3(Agent1):
    def __init__(self, location, graph):
        super().__init__(location)

        # initialize belief state such that there is equal probability that the prey is in every node except the agent's current one
        self.belief_state = dict()
        for i in range(1, graph.get_nodes() + 1):
            self.belief_state[i] = 1 / (graph.get_nodes() - 1) if i != self.location else 0

        # stores where prey was if we found it in the previous ste
        # starts at -1 to indicate we did not start yet
        self.prev_prey_location = -1

        # stores the num of times agent knows exactly where prey is
        num_times_know_exactly_where_prey_is = 0 

        print(f'GRAPH NEIGHBORS: {graph.get_neighbors()}')

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
        print(f'\nCURRENT LOCATION {self.location}')
        if self.prev_prey_location > 0:
            # because we found the prey last time, we need to update the probabilities to reflect the prey's potential locations
            print(
                "FOUND PREY PREVIOUSLY, UPDATING PROBABILITIES BASED ON POSSIBLE PREY MOVES")
            prey_possible_moves = graph.get_node_neighbors(self.prev_prey_location) + [self.prev_prey_location]
            if self.location in prey_possible_moves:
                prey_possible_moves.remove(self.location)

            self.belief_state = dict()
            for i in range(1, graph.get_nodes() + 1):
                self.belief_state[i] = 1 / \
                    (len(prey_possible_moves)) if i in prey_possible_moves else 0
        elif self.prev_prey_location == 0:
            # we did not find the prey last time, need to update the probabilities
            print("DIDN'T FIND PREY PREVIOUSLY, UPDATING PROBABILITIES")
            prev_prob_location = self.belief_state[self.location]
            for node, prob in self.belief_state.items():
                self.belief_state[node] = prob / \
                    (1 - prev_prob_location) if node != self.location else 0

        print(f'STARTING BELIEF STATE: {self.belief_state}')
        # sanity check that the belief state probabilities add up to 1
        # assert round(sum(self.belief_state.values()), 5) == 1

        # choose node to survey based on the nodes with the highest probability of containing the prey
        survey_node = random.choice(self.get_highest_prob_nodes())
        prey_found = True if prey.location == survey_node else False

        if prey_found:
            print(f'SURVEYED {survey_node}, PREY FOUND')
            # if prey was found, set probability of prey location 1 and everything else to 0
            for i in range(1, graph.get_nodes() + 1):
                self.belief_state[i] = 0 if i != survey_node else 1

            print(f'UPDATED BELIEF STATE: {self.belief_state}')

            # move according to the rules of agent 1
            super().move(graph, prey, predator)

            # set the location of the prey
            self.prev_prey_location = prey.location

            return 1
        else:
            print(f'SURVEYED {survey_node}, PREY NOT FOUND')
            # if prey was not found, update belief state based on derived update rule
            prob_survey_node = self.belief_state[survey_node]
            for node, prob in self.belief_state.items():
                self.belief_state[node] = prob / \
                    (1 - prob_survey_node) if node != survey_node else 0

            print(f'UPDATED BELIEF STATE: {self.belief_state}')

            # sanity check that the belief state probabilities add up to 1
            assert sum(self.belief_state.values()) == 1

            # select potential prey position and move according to the rules of agent 1
            highest_prob_nodes = self.get_highest_prob_nodes()
            potential_prey = Prey(random.choice(highest_prob_nodes))
            super().move(graph, potential_prey, predator)

            # set that we did not find the prey
            self.prev_prey_location = 0

            return 1

    def move_debug(self, graph, prey, predator):
        return 1
