import random
import networkx as nx
import matplotlib.pyplot as plt
from game.agents.agent1 import Agent1
from .graph import Graph
from .predator import Predator
from .prey import Prey


class Game:
    def __init__(self):
        self.graph = Graph(nodes=5)

        self.prey = Prey(random.randint(1, self.graph.get_nodes()))
        self.predator = Predator(random.randint(1, self.graph.get_nodes()))

        occupied_s = min(self.prey.location, self.predator.location)
        occupied_l = max(self.prey.location, self.predator.location)
        agent_location_options = list(range(1, occupied_s)) + list(range(
            occupied_s+1, occupied_l)) + list(range(occupied_l+1, self.graph.get_nodes() + 1))
        self.agent_starting_location = random.choice(agent_location_options)

        self.agent = None

    def step(self):
        """
        moves the agent, prey, and predator one step

        returns
        * 1 if agent wins
        * 0 if game in progress
        * -1 if agent looses 
        """
        self.agent.move(self.graph, self.prey, self.predator)

        self.prey.move(self.graph)
        if self.agent.location == self.prey.location:
            return 1

        self.predator.move(self.graph, self.agent)
        if self.agent.location == self.predator.location:
            return -1

        return 0

    def run_agent_1(self):
        self.agent = Agent1(self.agent_starting_location)
        self.visualize_graph()

        status = 0
        while status == 0:
            status = self.step()
            self.visualize_graph()

        return status

    def visualize_graph_color_map(self):
        color_map = ["grey" for _ in self.graph.get_neighbors()]
        color_map[self.prey.location - 1] = "yellowgreen"
        color_map[self.predator.location - 1] = "lightcoral"

        if self.agent is not None:
            color_map[self.agent.location - 1] = "gold"

        return color_map

    def visualize_graph(self, fn='environment.png'):
        """visualizes nodes and their edges with labels in non-circular layout"""
        plt.rcParams['figure.figsize'] = [8, 5]
        G = nx.from_dict_of_lists(self.graph.get_neighbors())
        my_pos = nx.spring_layout(G, seed = 100)
        nx.draw(G, pos = my_pos, node_color=self.visualize_graph_color_map(), with_labels=True)

        figure_text = "Agent: {}, Prey: {}, Predator: {}".format(
            self.agent.location, self.prey.location, self.predator.location)
        plt.figtext(0.5, 0.01, figure_text, ha="center", fontsize=8)

        plt.show()

    def visualize_graph_circle(self):
        """visualizes nodes and their edges with labels in a circular layout"""
        nx.draw_networkx(nx.Graph(self.graph.get_neighbors()), pos=nx.circular_layout(
            nx.Graph(self.graph.get_neighbors())), node_color=self.visualize_graph_color_map(), node_size=50, with_labels=True)
        plt.show()
