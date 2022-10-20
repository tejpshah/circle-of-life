import random 
from .agent import Agent 

class Agent1(Agent):
    def __init__(self, location):
        super().__init__(location)
        self.curr_prey_dist = 0
        self.curr_pred_dist = 0 
        self.nbrs_prey_dist = dict() 
        self.nbrs_pred_dist = dict()
    
    def move(self, graph, prey, predator):
        self.curr_prey_dist = self.bfs(graph, self.location, prey.location)
        self.curr_pred_dist = self.bfs(graph, self.location, predator.location)
        self.nbrs_prey_dist = dict() 
        self.nbrs_pred_dist = dict()

        nbrs = graph.get_node_neighbors(self.location)
        for nbr in nbrs: 
            self.nbrs_prey_dist[nbr] = self.bfs(graph, nbr, prey.location)
            self.nbrs_pred_dist[nbr] = self.bfs(graph, nbr, predator.location)
        
        status1, prey_closer = self.nbrs_closer_to_prey() 
        status2, pred_farther = self.nbrs_farther_from_pred() 
        status3, pred_notcloser = self.nbrs_not_closer_to_pred()
        status4, prey_notfarther = self.nbrs_not_farther_from_prey()

        seta, setb, candidates = set(), set(), []
        if status1 and status2:
            seta, setb = set(prey_closer), set(pred_farther)
            candidates =  list(seta.intersection(setb))
        if len(candidates) == 0 and status1 and status3: 
            seta, setb = set(prey_closer), set(pred_notcloser)
            candidates =  list(seta.intersection(setb))
        if len(candidates) == 0 and status4 and status2:
            seta, setb = set(prey_notfarther), set(pred_farther)
            candidates =  list(seta.intersection(setb))
        if len(candidates) == 0 and status4 and status3:
            seta, setb = set(prey_notfarther), set(pred_notcloser) 
            candidates =  list(seta.intersection(setb))
        if len(candidates) == 0 and status2:
            seta, setb = set(pred_farther), set(pred_farther)
            candidates =  list(seta.intersection(setb))
        if len(candidates) == 0 and status3:
            seta, setb = set(pred_notcloser), set(pred_notcloser) 
            candidates =  list(seta.intersection(setb))
        if len(candidates) == 0: 
            seta.add(self.location)
            setb.add(self.location)
            candidates =  list(seta.intersection(setb))
        self.location = random.choice(candidates)
        return 1 

    def move_debug(self, graph, prey, predator):
        self.curr_prey_dist = self.bfs(graph, self.location, prey.location)
        self.curr_pred_dist = self.bfs(graph, self.location, predator.location)
        self.nbrs_prey_dist = dict() 
        self.nbrs_pred_dist = dict()

        nbrs = graph.get_node_neighbors(self.location)
        for nbr in nbrs: 
            self.nbrs_prey_dist[nbr] = self.bfs(graph, nbr, prey.location)
            self.nbrs_pred_dist[nbr] = self.bfs(graph, nbr, predator.location)
        
        status1, prey_closer = self.nbrs_closer_to_prey() 
        status2, pred_farther = self.nbrs_farther_from_pred() 
        status3, pred_notcloser = self.nbrs_not_closer_to_pred()
        status4, prey_notfarther = self.nbrs_not_farther_from_prey()

        seta, setb, candidates = set(), set(), []
        if status1 and status2:
            seta, setb = set(prey_closer), set(pred_farther)
            candidates =  list(seta.intersection(setb))
            if len(candidates) > 0: 
                print("NEIGHBORS THAT ARE CLOSER TO PREY AND FARTHER FROM PREDATOR")
        if len(candidates) == 0 and status1 and status3: 
            seta, setb = set(prey_closer), set(pred_notcloser)
            candidates =  list(seta.intersection(setb))
            if len(candidates) > 0: 
                print("NEIGHBORS THAT ARE CLOSER TO PREY AND NOT CLOSER TO THE PREDATOR")
        if len(candidates) == 0 and status4 and status2:
            seta, setb = set(prey_notfarther), set(pred_farther)
            candidates =  list(seta.intersection(setb))
            if len(candidates) > 0:
                print("NEIGHBORS THAT ARE NOT FARTHER FROM PREY AND FARTHER FROM PREDATOR")
        if len(candidates) == 0 and status4 and status3:
            seta, setb = set(prey_notfarther), set(pred_notcloser) 
            candidates =  list(seta.intersection(setb))
            if len(candidates) > 0:
                print("NEIGHBORS THARE ARE NOT FARTHER FROM THE PREY AND FARTHER FROM PREDATOR")
        if len(candidates) == 0 and status2:
            seta, setb = set(pred_farther), set(pred_farther)
            candidates =  list(seta.intersection(setb))
            if len(candidates) > 0:
                print("!NEIGHBORS THAT ARE FARTHER FROM THE PREDATOR")
        if len(candidates) == 0 and status3:
            seta, setb = set(pred_notcloser), set(pred_notcloser) 
            candidates =  list(seta.intersection(setb))
            if len(candidates) > 0:
                print("!NEIGHBORS THAT ARE NOT CLOSER TO THE PREDATOR")
        if len(candidates) == 0: 
            seta.add(self.location)
            setb.add(self.location)
            candidates =  list(seta.intersection(setb))
            if len(candidates) > 0:
                print("!SIT STILL AND PRAY")

        print(f"CANDIDATES ARE: {candidates}")
        self.location = random.choice(candidates)
        print(f"NEW AGENT LOCATION IS: {self.location}")
        return 1 

    def nbrs_closer_to_prey(self):
        """
        returns all possible moves that are of less distance to the prey than current location.
        """
        possible_moves = []
        shortest_distance_from_prey = min(self.nbrs_prey_dist.values())
        if shortest_distance_from_prey < self.curr_prey_dist:
            for neighbor, distance in self.nbrs_prey_dist.items():
                if distance < self.curr_prey_dist:
                    possible_moves.append(neighbor)
            return True, possible_moves
        else: return False, possible_moves
    
    def nbrs_not_farther_from_prey(self):
        """
        returns all possible moves that are of less than or equal distance to the prey than current location.
        """
        possible_moves = []
        shortest_distance_from_prey = min(self.nbrs_prey_dist.values())
        if shortest_distance_from_prey <= self.curr_prey_dist:
            for neighbor, distance in self.nbrs_prey_dist.items():
                if distance <= self.curr_prey_dist:
                    possible_moves.append(neighbor)
            return True, possible_moves
        else: return False, possible_moves
    
    def nbrs_farther_from_pred(self):
        """
        returns all possible moves that are of greater distance to the predator than current location.
        """
        possible_moves = [] 
        maximum_distance_from_pred = max(self.nbrs_pred_dist.values())
        if maximum_distance_from_pred > self.curr_pred_dist:
            for neighbor, distance in self.nbrs_pred_dist.items():
                if distance > self.curr_pred_dist:
                    possible_moves.append(neighbor)
            return True, possible_moves
        else: return False, possible_moves 

    def nbrs_not_closer_to_pred(self):
        """
        returns all possible moves that are of distance greater than or equal to the current distance to predator. 
        """
        possible_moves = [] 
        maximum_distance_from_pred = max(self.nbrs_pred_dist.values())
        if maximum_distance_from_pred >= self.curr_pred_dist:
            for neighbor, distance in self.nbrs_pred_dist.items():
                if distance >= self.curr_pred_dist:
                    possible_moves.append(neighbor)
            return True, possible_moves
        else: return False, possible_moves 

