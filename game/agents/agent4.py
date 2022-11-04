import random
from copy import deepcopy
from game.prey import Prey
from .agent2 import Agent2


class Agent4(Agent2):
    def __init__(self, location, graph):
        # initialize agent location
        super().__init__(location)

        # initializes agent belief prob dist
        self.init_probs_step1(graph)

        # list of all prey prev locations
        self.prev_prey_locations = []

    def move(self, graph, prey, predator):
        """
        surveys the node with the highest probability of containing the prey
        updates the beliefs
        * if signal is false and we have previously not found prey, reinitialize beliefs to 1/(n - 2) for all nodes other than surveyed and agent current location
        * if signal is false and we have previously found prey, update beliefs based on probability that the prey could be in each position
        * if signal is true, beliefs is a one-hot vector
        assume the prey is at one of the locations with the highest probability, chosen based on farthest distance from predator
        move according to the rules of agent2 
        """
        signal, surveyed_node = self.survey_node(prey)
        if len(self.prev_prey_locations) == 0:
            self.init_probs_step2(graph, surveyed_node)
        elif signal == True and len(self.prev_prey_locations) > 0:
            self.init_probs_step3(surveyed_node)
        elif signal == False and len(self.prev_prey_locations) > 0:
            self.init_probs_step4(graph, surveyed_node)
        self.normalize_beliefs()

        # SELECT NODE WITH HIGHEST PROBABILITY FARTHEST FROM PREDATOR TO MOVE TO
        node_pred_dist = {node: self.bfs(
            graph, node, predator.location) for node in self.get_highest_prob_nodes()}
        highest_pred_dist_nodes = [node for node, dist in node_pred_dist.items(
        ) if dist == max(node_pred_dist.values())]
        node = random.choice(highest_pred_dist_nodes)
        potential_prey = Prey(node)

        super().move(graph, potential_prey, predator)
        return len(self.prev_prey_locations), None

    def move_debug(self, graph, prey, predator):
        """
        debug version of move
        """
        signal, surveyed_node = self.survey_node(prey)
        print(f"\nTHE SIGNAL IS {signal} for surveyed node {surveyed_node}")
        print(f"The agent's current location is {self.location}")

        print(f"\nPRIOR BELIEFS: \n{self.beliefs}")

        if len(self.prev_prey_locations) == 0:
            print("UPDATED PROBABILITIES INIT 2")
            self.init_probs_step2(graph, surveyed_node)

        elif signal == True and len(self.prev_prey_locations) > 0:
            print("UPDATED PROBABILITIES INIT 3")
            self.init_probs_step3(surveyed_node)

        elif signal == False and len(self.prev_prey_locations) > 0:
            print("UPDATED PROBABILITIES INIT 4")
            print(f"CURRENT FRONTIER: {self.frontier}")
            print(f"GRAPH NEIGHBORS:  {graph.nbrs}")
            self.init_probs_step4(graph, surveyed_node)

        self.normalize_beliefs()
        print(f"THE SUM OF THE PROBABILITIES IS {sum(self.beliefs.values())}")
        self.round_belief_probs()
        print(f"UPDATED BELIEFS: \n{self.beliefs}\n")

        # SELECT NODE WITH HIGHEST PROBABILITY FARTHEST FROM PREY TO MOVE TO
        node_pred_dist = {node: self.bfs(
            graph, node, predator.location) for node in self.get_highest_prob_nodes()}
        highest_pred_dist_nodes = [node for node, dist in node_pred_dist.items(
        ) if dist == max(node_pred_dist.values())]
        node = random.choice(highest_pred_dist_nodes)
        potential_prey = Prey(node)

        super().move(graph, potential_prey, predator)
        return len(self.prev_prey_locations), None

    def init_probs_step1(self, graph):
        """
        CORE: INITIALIZING INITIAL PROBABILITY.

        BELIEF UPDATE STEP 1: 
        P(n_i) = 1 / (n-1) for every node not containing agent 
        P(n_k) = 0 for the kth node containing the agent
        """
        self.beliefs = dict()
        for i in range(1, graph.get_nodes() + 1):
            if i == self.location:
                self.beliefs[i] = 0
            else:
                self.beliefs[i] = 1 / (graph.get_nodes() - 1)

    def init_probs_step2(self, graph, surveyed_node):
        """
        CORE: SURVEYED NODE BUT THE PREY IS NOT THERE AND WE HAVEN'T FOUND PREY BEFORE. 

        BELIEF UPDATE STEP 2: 
        P(n_i) = 1 / (n-2) for every node not agent's current location or surveyed_node
        P(n_k) = P(n_surveyed) = 0 for the kth node containing the agent and the surveyed node
        """
        for node, _ in self.beliefs.items():
            if node == self.location or node == surveyed_node:
                self.beliefs[node] = 0
            else:
                self.beliefs[node] = 1 / (graph.get_nodes() - 2)

    def init_probs_step3(self, surveyed_node):
        """
        CORE: SURVEYED NODE CONTAINS PREY!

        BELIEF UPDATE STEP 3: 
        P(n_surveyed) = 1
        P(n_i) = 0 for all i != n_surveyed
        """
        for node, _ in self.beliefs.items():
            if node == surveyed_node:
                self.beliefs[node] = 1
            else:
                self.beliefs[node] = 0

        # SETS UP FRONTIER OF UNIQUE STATES VISITED FOR BELIEF UPDATE 4
        self.frontier = set()
        self.frontier.add(surveyed_node)

        # ADDS IT TO PREVOIUS PREY LOCATIONS SEEN
        self.prev_prey_locations.append(surveyed_node)

    def init_probs_step4(self, graph, surveyed_node):
        """
        CORE: SURVEYED NODE DOESN'T CONTAIN PREY BUT WE FOUND A PREY BEFORE!

        BELIEF UPDATE STEP 4: 
        - Given frontier F_{t-1} at t-1, determine frontier F_{t} at t, and compute # of ways to get to each element in F_{t}
        - Remove the number of ways to get to current agent location if exists in set or current surveyed node if it exists in set
        - Update beliefs based on the number of ways to get to each place in a particular state
        """

        # RETRIEVES THE FREQUENCY EACH STATE CAN BE VISITED FROM FRONTIER
        counts = dict()
        for node in self.frontier:
            counts[node] = counts.get(node, 0) + 1
            for nbr in graph.nbrs[node]:
                counts[nbr] = counts.get(nbr, 0) + 1

        # UDPATES FRONTIER, ALL POSSIBLE STATES AGENT CAN BE IN
        self.frontier = set(counts.keys())

        # WE COMPUTE THE PROBABILITIES BASED ON FREQUENCY
        probability_mass = deepcopy(counts)
        probability_mass[self.location] = 0
        probability_mass[surveyed_node] = 0
        denominator = sum(probability_mass.values())

        # UPDATE THE BELIEFS BASED ON FREQUENCIES
        for key in probability_mass.keys():
            self.beliefs[key] = probability_mass[key] / denominator
        for key in self.beliefs.keys():
            if key not in probability_mass:
                self.beliefs[key] = 0

    def normalize_beliefs(self):
        """
        ENSURES THAT ALL PROBABILITIES SUM TO 1
        """
        values_sum = sum(self.beliefs.values())
        for node, probability in self.beliefs.items():
            self.beliefs[node] = probability/values_sum

    def survey_node(self, prey):
        """
        HELPER:
        RETURNS (SIGNAL=T/F, NODE_SURVEYED=n_i)
        Indicates node surveyed and whether or not prey is there. 
        """
        signal = False
        node = random.choice(self.get_highest_prob_nodes())
        if prey.location == node:
            signal = True
            self.prev_prey_locations.append(node)
        return signal, node

    def get_highest_prob_nodes(self):
        """
        HELPER:
        RETURNS LIST OF ALL NODES OF EQUIVALENT HIGHEST PROBABILITY. 
        """
        PROB, nodes = max(self.beliefs.values()), []
        for node, prob in self.beliefs.items():
            if prob == PROB:
                nodes.append(node)
        return nodes

    def round_belief_probs(self, k=4):
        """
        HELPER:
        UPDATES ALL BELIEFS TO BE ROUNDED TO K DECIMAL PLACES.
        """
        for key in self.beliefs.keys():
            self.beliefs[key] = round(self.beliefs[key], k)
