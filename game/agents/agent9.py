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
