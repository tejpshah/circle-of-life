import random 
from .agent1 import Agent1 
from copy import deepcopy 
from game.predator import Predator 
from game.prey import Prey 

class Agent7(Agent1):
    def __init__(self, location, graph, predator):
        super().__init__(location)

        self.prev_preds = [] 
        self.prev_preys = [] 

        self.prey_beliefs = dict() 
        self.pred_beliefs = dict() 

        self.init_belief_probs_1(graph, predator)
    
    def init_belief_probs_1(self, graph, predator):
        for i in range(1, graph.get_nodes() + 1):
            if i == self.location: self.prey_beliefs[i] = 0 
            else: self.prey_beliefs[i] = 1 / (graph.get_nodes() - 1)
        for i in range(1, graph.get_nodes() + 1):
            if i == predator.location: self.pred_beliefs[i] = 1 
            else: self.pred_beliefs[i] = 0 

    def survey_node(self, graph, prey, predator):
        prey_signal, pred_signal, node = False, False, 0 
        is_certain_where_pred_is = len({self.pred_beliefs[i] for i in range(1, graph.get_nodes()+1) if self.pred_beliefs[i] == 1}) == 1 

        if not is_certain_where_pred_is: 
            highest_prob_pred_nodes = self.get_highest_prob_pred_nodes()
            node = random.choice(highest_prob_pred_nodes)
        elif is_certain_where_pred_is:
            highest_prob_prey_nodes = self.get_highest_prob_prey_nodes() 
            node = random.choice(highest_prob_prey_nodes)
        
        if predator.location == node: 
            pred_signal = True 
            self.prev_preds.append(node)
        if prey.location == node: 
            prey_signal = True 
            self.prev_preys.append(node)

        return prey_signal, pred_signal, node 
    
    def get_highest_prob_pred_nodes(self):
        PROB, nodes = max(self.pred_beliefs.values()), [] 
        for node, prob in self.pred_beliefs.items(): 
            if prob == PROB: nodes.append(node)
        return nodes 
    
    def get_highest_prob_prey_nodes(self):
        PROB, nodes = max(self.prey_beliefs.values()), [] 
        for node, prob in self.prey_beliefs.items(): 
            if prob == PROB: nodes.append(node)
        return nodes 
    
