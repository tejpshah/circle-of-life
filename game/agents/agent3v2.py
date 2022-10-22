import random
from .agent1 import Agent1
from game.prey import Prey
from copy import deepcopy

class Agent3(Agent1):
    def __init__(self, location, graph):

        # initializes A3 with given location 
        super().__init__(location)

        print(1 / graph.get_nodes()-1)

        # intializes belief states to be 1 / (N-1) for probability of prey for every cell that is not the agent
        self.beliefs = {i:round((1/ (graph.get_nodes()-1)), 4) for i in range(1, graph.get_nodes()+1) if i != self.location}

        print(self.beliefs)

        # a list that stores the prey's previous locations whenever it is completely known for sure 
        self.prey_prev_locations = [] 

        # keeps track of the nodes that we need in frontier for redistributing probability mass
        self.frontier = set() 

        # keeps track of counts and frequencies for redistributing the probability mass
        self.counts = dict() 

    def get_highest_prob_nodes(self):
        """gets nodes that have the highest probability of containing the prey"""
        highest_prob = max(self.beliefs.values())
        highest_prob_nodes = []
        for node, prob in self.beliefs.items():
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

    def update_probs_with_bayes(self, highest_prob_node):
        """
        P(n_i = True | n_curr = False) = P(n_i = True) * P(n_curr = False | n_i = True) / P(n_curr = False)
        P(n_i = True | n_curr = False) = P(n_i = True) * 1 / P(n_curr = False)
        P(n_i = True | n_curr = False) = P(n_i = True) * 1 / (1-P(n_curr = True))
        avoid divide by zero errors if at any point denom becomes arbitrarily close to 0
        """
        denominator = max(1 - self.beliefs[highest_prob_node], 0.0001)
        for node, prior in self.beliefs.items():
            if node == self.location or node == highest_prob_node: self.beliefs[node] = 0 
            else: self.beliefs[node] = round(prior / denominator, 4)

    def update_probs_found_prey(self, highest_prob_node):
        """update probabilities according to one hot vector {0,0,0,...,1,....,0}"""
        for node, belief in self.beliefs.items():
            self.beliefs[node] = 0 if node != highest_prob_node else 1 
        self.frontier.add(highest_prob_node)
        self.counts = dict() 

    def update_probs_found_prey_distribute_probability(self, graph, highest_prob_node):
        """redistribute probability mass"""
        new_frontier = set() 
        for node in self.frontier:  
            self.counts[node] = self.counts.get(node,0) + 1 
            new_frontier.add(node)
            for nbr in graph.nbrs[node]:
                self.counts[nbr] = self.counts.get(nbr,0) + 1 
                new_frontier.add(nbr)
        self.frontier = new_frontier

        probability_mass = deepcopy(self.counts)
        probability_mass[self.location] = 0
        probability_mass[highest_prob_node] = 0 

        normalization_denominator = sum(probability_mass.values())
        for key in probability_mass.keys():
            self.beliefs[key] = round(probability_mass[key] / normalization_denominator, 4)


    def move(self, graph, prey, predator):
        """
        # take a signal reading of the highest proability node to see if a prey exists 
        # uncertain where prey is at all so all we have to update beliefs is Bayes Rule.
        # we've previously had a signal reading of where the prey actually is 
            # if the current timestep's signal is the prey, update all the proabilities: {0,0,...,1,...,0}
            # otherwise, propogate probability mass of beliefs to neighbors, neighbors of neighbors, and so on (modified bfs)
        """
        signal, highest_prob_node = self.get_signal_prey_exists(prey)

        if len(self.prey_prev_locations) == 0: 
            """while we do not know where the prey is, update the probabilities of all nodes with Bayes Rule"""
            self.update_probs_with_bayes(highest_prob_node)
            print(f"UPDATING WITH BAYES RULE:{self.beliefs}\n")

        elif signal == True and len(self.prey_prev_locations) > 0 : 
            """update probabilities according to one hot vector {0,0,0,...,1,....,0}"""
            self.update_probs_found_prey(highest_prob_node)
            print(f"FOUND PREY:{self.beliefs}\n")

        elif signal == False and len(self.prey_prev_locations) > 0:
            """redistribute the probability mass based on the number of timesteps since last seen""" 
            print(f"PROPOGATE PREY BELIEFS:{self.beliefs}\n")
            self.update_probs_found_prey_distribute_probability(graph, highest_prob_node)

        # select potential prey position and move according to the rules of agent 1
        highest_prob_nodes = self.get_highest_prob_nodes()
        potential_prey = Prey(random.choice(highest_prob_nodes))
        super().move(graph, potential_prey, predator)

        return 1 

    def move_debug(self, graph, prey, predator):
        return 1 
  
