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

    def move(self, graph, prey, predator):
        """
        # take a signal reading of the highest proability node to see if a prey exists 
        # uncertain where prey is at all so all we have to update beliefs is Bayes Rule.
        # we've previously had a signal reading of where the prey actually is 
            # if the current timestep's signal is the prey, update all the proabilities: {0,0,...,1,...,0}
            # otherwise, propogate probability mass of beliefs to neighbors, neighbors of neighbors, and so on (modified bfs)
        """


        if len(self.prey_prev_locations) == 0: 
            pass 


        else: 
            pass 



  
