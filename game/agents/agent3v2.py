import random
from .agent1 import Agent1
from game.prey import Prey

class Agent3(Agent1):
    def __init__(self, location, graph):

        # initializes A3 with given location 
        super().__init__(location)

        # intializes belief states to be 1 / (N-1) for probability of prey for every cell that is not the agent
        self.beliefs = {i:round((1/graph.get_nodes()-1), 4) for i in range(1, graph.get_nodes()+1) if i != self.location}

        # a list that stores the prey's previous locations whenever it is completely known for sure 
        self.prey_prev_locations = [] 

    def get_highest_prob_nodes(self):
        """gets nodes that have the highest probability of containing the prey"""
        highest_prob = max(self.belief_state.values())
        highest_prob_nodes = []
        for node, prob in self.belief_state.items():
            if prob == highest_prob:
                highest_prob_nodes.append(node)
        return highest_prob_nodes
    
    def get_signal_prey_exists(self, prey):
        """returns whether or not a prey exists at a location"""
        signal = False 
        node = random.choice(self.get_highest_prob_nodes())
        if prey.location == node: 
            signal = True
            self.prey_prev_locations.append(node)
        return signal, node 

    def update_probs_with_bayes(self, node):
        # P(n_i = True | n_curr = False) = P(n_i = True) * P(n_curr = False | n_i = True) / P(n_curr = False)
        # P(n_i = True | n_curr = False) = P(n_i = True) * 1 / P(n_curr = False)
        # P(n_i = True | n_curr = False) = P(n_i = True) * 1 / (1-P(n_curr = True))
        # avoid divide by zero errors if at any point denom becomes arbitrarily close to 0

        denominator = min(1 - self.beliefs[node], 0.0001)
        for node, prior in self.beliefs.items():
            if node == self.location: self.beliefs[node] = 0 
            else: self.beliefs[node] = prior / denominator 

    def move(self, graph, prey, predator):
        """
        # take a signal reading of the highest proability node to see if a prey exists 
        # uncertain where prey is at all so all we have to update beliefs is Bayes Rule.
        # we've previously had a signal reading of where the prey actually is 
            # if the current timestep's signal is the prey, update all the proabilities: {0,0,...,1,...,0}
            # otherwise, propogate probability mass of beliefs to neighbors, neighbors of neighbors, and so on (modified bfs)
        """
        signal, node = self.get_signal_prey_exists(prey)
        if len(self.prey_prev_locations) == 0: 
            """while we do not know where the prey is, update the probabilities of all nodes with Bayes Rule"""
            self.update_probs_with_bayes(node)
        elif signal == True and len(self.prey_prev_locations) > 0 : 
            """update probabilities according to one hot vector {0,0,0,...,1,....,0}"""



            pass 
        elif signal == False and len(self.prey_prev_locations) > 0:
            pass 
            


        else: 
            """while we previously know where the prey is"""
            pass 



  
