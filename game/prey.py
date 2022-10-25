"""
SANITY CHECKED: PREY SHOULD BE WORKING AS SPECIFIED PER ASSIGNMENT DESCRIPTION.
"""

import random


class Prey:
    def __init__(self, location):
        self.location = location

    def move(self, graph):
        """
        selects among its neighbors or its current cell, uniformly at random, to determine its next step
        """
        # get list of neighbors
        neighbors = graph.get_node_neighbors(self.location)

        # choose location at random while also considering current location
        possible_moves = neighbors + [self.location]
        new_location = random.choice(possible_moves)

        # move to to the new location
        self.location = new_location

    def move_debug(self, graph):
        """
        -- debug method -- 
        selects among its neighbors or its current cell, uniformly at random, to determine its next step
        """
        print("\nPrey Move")
        print("Current Location: " + str(self.location))

        # get list of neighbors
        neighbors = graph.get_node_neighbors(self.location)
        print("Current Neighbors: " + str(neighbors))

        # choose location at random while also considering current location
        possible_moves = neighbors + [self.location]
        print("Possible Moves: " + str(possible_moves))
        new_location = random.choice(possible_moves)
        print("Chosen Location: " + str(new_location))

        # move to to the new location
        self.location = new_location
        print("Moved Location: " + str(self.location))
