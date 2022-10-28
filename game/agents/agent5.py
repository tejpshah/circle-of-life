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

    def init_probs_step3(self, surveyed_node):
        """
        CORE: REDISTRIBUTE PROBABILITY MASS AND UPDATE THE FRONTIER. 
        """