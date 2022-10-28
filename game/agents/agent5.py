from math import dist
import random 
from .agent1 import Agent1 
from game.predator import Predator
from copy import deepcopy 

class Agent5(Agent1):
    def __init__(self, location, graph, predator):
        # initiailize agent location 
        super().__init__(location)

        # initialize probs of predator 
        self.init_probs_step1(graph, predator)

        # list of all pred prev locations
        self.pred_prev_locations = [] 
    
    def move(self, graph, prey, predator):
        signal, surveyed_node = self.survey_node(predator)
        if signal == True: self.init_probs_step1(graph, predator)
        elif signal == False: self.init_probs_step2(graph, surveyed_node)
        self.normalize_beliefs()

        potential_predator = Predator(random.choice(self.get_highest_prob_nodes()))
        super().move(graph, prey, potential_predator)
        return None, len(self.pred_prev_locations)

    def init_probs_step1(self, graph, predator):
        """
        CORE: SETS PROBABILITY OF WHERE PREDATOR IS TO 1, 0 EVERYWHERE ELSE. 
        IF SiGNAL IS TRUE FOR WHERE THE PREDATOR IS, THEN CALL THIS FUNCTION TOO!
        """
        self.beliefs = dict()
        for i in range(1, graph.get_nodes() + 1):
            if i == predator.location: self.beliefs[i] = 1
            else: self.beliefs[i] = 0 
        
        # SETS UP THE CURRENT FRONTIER FOR PROBABILITY MASS REDISTRIBUTION
        self.frontier = set() 
        self.frontier.add(predator.location)

        # WE FOUND THE PREDATOR!
        self.pred_prev_locations.append(predator.location)

    def init_probs_step2(self, graph, surveyed_node):
        """
        CORE: REDISTRIBUTE PROBABILITY MASS AND UPDATE THE FRONTIER. 
        - Given frontier F_{t-1} at t-1, determine frontier F_{t} at t, and compute # of ways to get to each element in F_{t}
        - Remove the number of ways to get to current agent location if exists in set or current surveyed node if it exists in set
        - Update beliefs based on the number of ways to get to each place in a particular state
        """

        # FIND ALL THE COUNTS TO EACH NEIGHBOR IN THE POSSIBLE FRONTIER
        counts = dict() 
        for node in self.frontier: 
            counts[node] = counts.get(node, 0) + 1 
            for nbr in graph.nbrs[node]:
                counts[nbr] = counts.get(nbr, 0) + 1 

        # FIND ALL THE DISTANCES FOR EACH POSSIBLE NEIGHBOR IN THE FRONTIER
        distances = {}  
        for state in self.frontier:
            distances[state] = min(distances.get(state, float("inf")), self.bfs(graph, self.location, state))
            for nbr in graph.nbrs[state]:
                distances[nbr] = min(distances.get(nbr, float("inf")), self.bfs(graph, self.location, nbr))
        
        # FIND OUT ALL POSSIBLE OPTIMAL SOLUTIONS THAT CAN BE TAKEN
        min_dist = min(distances.values())
        pruned = {}
        for key, dist in distances.items():
            if dist == min_dist: pruned[key] = counts[key] 

        # UPDATE THE FRONTIER TO ONLY BE THE POTENTIAL OPTIMAL LOCATIONS
        self.frontier = set(pruned.keys())

        # WE COMPUTE THE PROBABILITIES BASED ON FREQUENCY
        probability_mass = deepcopy(counts)
        probability_mass[self.location] = 0 
        probability_mass[surveyed_node] = 0 
        denominator = sum(probability_mass.values())

        # UPDATE THE BELIEFS BASED ON FREQUENCIES
        for key in probability_mass.keys(): 
            self.beliefs[key] = probability_mass[key] / denominator 
        for key in self.beliefs.keys():
            if key not in probability_mass: self.beliefs[key] = 0 

    def normalize_beliefs(self):
        """
        ENSURES THAT ALL PROBABILITIES SUM TO 1
        """
        values_sum = sum(self.beliefs.values())
        for node, probability in self.beliefs.items():
            self.beliefs[node] = probability/values_sum
        
    def survey_node(self, predator):
        """
        HELPER:
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
            if prob == PROB: nodes.append(node)
        return nodes 
    
    def round_belief_probs(self, k=4):
        """
        HELPER:
        UPDATES ALL BELIEFS TO BE ROUNDED TO K DECIMAL PLACES.
        """
        for key in self.beliefs.keys(): 
            self.beliefs[key] = round(self.beliefs[key], k)
