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

        self.pred_frontier = set() 
        self.pred_frontier.add(predator.location)
        self.prey_frontier = set()
    
    def move(self, graph, prey, predator):
        prey_signal, pred_signal, surveyed_node = self.survey_node(graph, prey, predator) 

        if len(self.prev_preys) == 0: 
            self.prey_belief_update_1(graph, surveyed_node)
        elif prey_signal == True and len(self.prev_preys) > 0: 
            self.prey_belief_update_2(surveyed_node)
        elif prey_signal == False and len(self.prev_preys) > 0: 
            self.prey_belief_update_3(graph, surveyed_node)

        if pred_signal == True: self.pred_belief_update_1(graph, surveyed_node)
        elif pred_signal == False: self.pred_belief_update_2(graph, surveyed_node)

        self.normalize_beliefs() 
        potential_prey = Prey(random.choice(self.get_highest_prob_prey_nodes()))
        potential_pred = Predator(random.choice(self.get_highest_prob_pred_nodes()))
        super().move(graph, potential_prey, potential_pred)
        return len(self.prev_preys), len(self.prev_preds)

    def move_debug(self, graph, prey, predator):
        prey_signal, pred_signal, surveyed_node = self.survey_node(graph, prey, predator) 
        print(f"\nWE SURVEYED NODE: {surveyed_node}\t Prey Signal: {prey_signal} \t Pred Signal: {pred_signal}\n")

        print(f"\nTHE PREY BELIEFS ARE BEFORE: {self.prey_beliefs}\n")
        print(f"\nTHE PRED BELIEFS ARE BEFORE: {self.pred_beliefs}\n")

        if len(self.prev_preys) == 0: 
            print("PREY BELIEF UPDATE: 1/48 Everywhere")
            self.prey_belief_update_1(graph, surveyed_node)
        elif prey_signal == True and len(self.prev_preys) > 0: 
            print("PREY BELIEF UPDATE: FOUND PREY!")
            self.prey_belief_update_2(surveyed_node)
        elif prey_signal == False and len(self.prev_preys) > 0: 
            print("PREY BELIEF UPDATE: DISTRIBUTE PROBS MASS")
            self.prey_belief_update_3(graph, surveyed_node)

        if pred_signal == True: 
            print("PRED BELIEF UPDATE: FOUND PREY")
            self.pred_belief_update_1(graph, surveyed_node)
        elif pred_signal == False: 
            print("PRED BELIEF UPDATE: DISTRIBUTE PROBS MASS")
            self.pred_belief_update_2(graph, surveyed_node)
        self.normalize_beliefs() 

        print(f"\nTHE PREY BELIEFS ARE NOW: {self.prey_beliefs}\n")
        print(f"\nTHE PRED BELIEFS ARE NOW: {self.pred_beliefs}\n")

        potential_prey = Prey(random.choice(self.get_highest_prob_prey_nodes()))
        potential_pred = Predator(random.choice(self.get_highest_prob_pred_nodes()))

        print(f"\nTHE ACTUAL AGENT IS AT {self.location}")
        print(f"THE POTENTIAL PREY IS AT {potential_prey.location}")
        print(f"THE POTENTIAL PRED IS AT {potential_pred.location}")
        print(f"THE ACTUAL PREY IS AT {prey.location}")
        print(f"THE ACTUAL PRED IS AT {predator.location}\n")

        super().move(graph, potential_prey, potential_pred)

        print(f"THE AGENT NOW MOVES TO {self.location}")

        return len(self.prev_preys), len(self.prev_preds)

    def init_belief_probs_1(self, graph, predator):
        for i in range(1, graph.get_nodes() + 1):
            if i == self.location: self.prey_beliefs[i] = 0 
            else: self.prey_beliefs[i] = 1 / (graph.get_nodes() - 1)
        for i in range(1, graph.get_nodes() + 1):
            if i == predator.location: self.pred_beliefs[i] = 1 
            else: self.pred_beliefs[i] = 0 

    def survey_node(self, graph, prey, predator):
        prey_signal, pred_signal, node = False, False, 0 


        boolean_set = {self.pred_beliefs[i] for i in range(1, graph.get_nodes()+1) if self.pred_beliefs[i] == 1}
        is_certain_where_pred_is = len(boolean_set) == 1 

        #print(f"THE BOOLEAN SET IS: {boolean_set} \t is_certain_where_pred_is={is_certain_where_pred_is}")

        if not is_certain_where_pred_is: 
            #print("WE ARE NOT CERTAIN WHERE PREDATOR IS SO WE SURVEY WRT A5!")
            highest_prob_pred_nodes = self.get_highest_prob_pred_nodes()
            node = random.choice(highest_prob_pred_nodes)
        elif is_certain_where_pred_is:
            #print("WE ARE CERTAIN WHERE PREDATOR IS AND NOT PREY SO WE SURVEY WRT A3")
            highest_prob_prey_nodes = self.get_highest_prob_prey_nodes() 
            node = random.choice(highest_prob_prey_nodes)
        
        if predator.location == node: 
            pred_signal = True 
            self.prev_preds.append(node)
        if prey.location == node: 
            prey_signal = True 
            self.prev_preys.append(node)

        return prey_signal, pred_signal, node 
    
    def prey_belief_update_1(self, graph, surveyed_node):
        for node, _ in self.prey_beliefs.items(): 
            if node == self.location or node == surveyed_node: self.prey_beliefs[node] = 0 
            else: self.prey_beliefs[node] = 1 / (graph.get_nodes() - 2)
    
    def prey_belief_update_2(self, surveyed_node):
        for node, _ in self.prey_beliefs.items():
            if node == surveyed_node: self.prey_beliefs[node] = 1
            else: self.prey_beliefs[node] = 0     
        self.prey_frontier = set() 
        self.prey_frontier.add(surveyed_node)
    
    def prey_belief_update_3(self, graph, surveyed_node):
        counts = dict()
        for node in self.prey_frontier: 
            counts[node] = counts.get(node, 0) + 1 
            for nbr in graph.nbrs[node]:
                counts[nbr] = counts.get(nbr, 0) + 1 
        self.prey_frontier = set(counts.keys())

        probability_mass = deepcopy(counts)
        probability_mass[self.location] = 0 
        probability_mass[surveyed_node] = 0 
        denominator = sum(probability_mass.values())

        for key in probability_mass.keys(): 
            self.prey_beliefs[key] = probability_mass[key] / denominator 
        for key in self.prey_beliefs.keys():
            if key not in probability_mass: self.prey_beliefs[key] = 0 

    def pred_belief_update_1(self, graph, surveyed_node):
        self.pred_frontier = set() 
        self.pred_frontier.add(surveyed_node)

        self.prev_preds.append(surveyed_node)

        def get_countshashmap_neighbor_frontier():
            counts = dict() 
            for node in self.pred_frontier: 
                counts[node] = counts.get(node, 0) + 1 
                for nbr in graph.nbrs[node]:
                    counts[nbr] = counts.get(nbr, 0) + 1 
            return counts 
        
        def get_distancehasmap_neighbor_frontier():
            distances = {}  
            for state in self.pred_frontier:
                distances[state] = min(distances.get(state, float("inf")), self.bfs(graph, self.location, state))
                for nbr in graph.nbrs[state]:
                    distances[nbr] = min(distances.get(nbr, float("inf")), self.bfs(graph, self.location, nbr))
            if self.location in distances: distances[self.location] = float("inf")
            if surveyed_node in distances: distances[surveyed_node] = float("inf")
            return distances 
        
        def get_possible_optimal_solutions(counts, distances):
            """FIND OUT ALL POSSIBLE OPTIMAL SOLUTIONS THAT CAN BE TAKEN"""
            pruned = {}
            for state in self.pred_frontier: 
                d = {} 
                d[state] = min(d.get(state, float("inf")), self.bfs(graph, self.location, state))
                for nbr in graph.nbrs[state]:
                    d[nbr] = min(d.get(nbr, float("inf")), self.bfs(graph, self.location, nbr))
                
                min_dist = min(d.values())
                for key in d: 
                    if d[key] == min_dist:
                        pruned[key] = counts[key]
            return pruned 

        counts = get_countshashmap_neighbor_frontier()
        distances = get_distancehasmap_neighbor_frontier()
        pruned = get_possible_optimal_solutions(counts, distances)
        self.pred_frontier = set(pruned.keys())

        probability_mass = deepcopy(pruned)
        denominator = sum(probability_mass.values())

        for key in self.pred_beliefs.keys():
            if key not in probability_mass: self.pred_beliefs[key] = 0 
            else: self.pred_beliefs[key] = probability_mass[key] / denominator 

    def pred_belief_update_2(self, graph, surveyed_node):
        def get_countshashmap_neighbor_frontier():
            counts = dict() 
            for node in self.pred_frontier: 
                counts[node] = counts.get(node, 0) + 1 
                for nbr in graph.nbrs[node]:
                    counts[nbr] = counts.get(nbr, 0) + 1 
            return counts 
        
        def get_distancehasmap_neighbor_frontier():
            distances = {}  
            for state in self.pred_frontier:
                distances[state] = min(distances.get(state, float("inf")), self.bfs(graph, self.location, state))
                for nbr in graph.nbrs[state]:
                    distances[nbr] = min(distances.get(nbr, float("inf")), self.bfs(graph, self.location, nbr))
            if self.location in distances: distances[self.location] = float("inf")
            if surveyed_node in distances: distances[surveyed_node] = float("inf")
            return distances 
        
        def get_possible_optimal_solutions(counts, distances):
            pruned = {}
            for state in self.pred_frontier: 
                d = {} 
                d[state] = min(d.get(state, float("inf")), self.bfs(graph, self.location, state))
                for nbr in graph.nbrs[state]:
                    d[nbr] = min(d.get(nbr, float("inf")), self.bfs(graph, self.location, nbr))
                
                min_dist = min(d.values())
                for key in d: 
                    if d[key] == min_dist:
                        pruned[key] = counts[key]
            return pruned 

        #print(self.pred_frontier)
        counts = get_countshashmap_neighbor_frontier()
        #print(counts)
        distances = get_distancehasmap_neighbor_frontier()
        #print(distances)
        pruned = get_possible_optimal_solutions(counts, distances)
        #print(pruned)
        self.pred_frontier = set(pruned.keys())
        #print(self.pred_frontier)

        probability_mass = deepcopy(pruned)
        #print(probability_mass)
        denominator = sum(probability_mass.values())

        for key in self.pred_beliefs.keys():
            if key not in probability_mass: self.pred_beliefs[key] = 0 
            else: self.pred_beliefs[key] = probability_mass[key] / denominator 

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
    
    def normalize_beliefs(self):
        values_sum = sum(self.pred_beliefs.values())
        for node, probability in self.pred_beliefs.items():
            self.pred_beliefs[node] = probability/ max(values_sum, 1)
        values_sum = sum(self.prey_beliefs.values())
        for node, probability in self.prey_beliefs.items():
            self.prey_beliefs[node] = probability/values_sum