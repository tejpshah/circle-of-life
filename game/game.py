import random
import networkx as nx
import matplotlib.pyplot as plt
from game.agents.agent1 import Agent1
from game.agents.agent2 import Agent2
from .graph import Graph
from .predator import Predator
from .prey import Prey


class Game:
    def __init__(self, nodes=50):

        # initializes the graph on which agents/prey/predator play
        self.graph = Graph(nodes=nodes)

        # initializes prey/predator locations to be random from nodes 1...50
        self.prey = Prey(random.randint(1, self.graph.get_nodes()))
        self.predator = Predator(random.randint(1, self.graph.get_nodes()))

        # agent initializes randomly to any spot that is not occupied by predator/prey
        occupied_s = min(self.prey.location, self.predator.location)
        occupied_l = max(self.prey.location, self.predator.location)
        agent_location_options = list(range(1, occupied_s)) + list(range(occupied_s+1, occupied_l)) + list(range(occupied_l+1, self.graph.get_nodes() + 1))
        self.agent_starting_location = random.choice(agent_location_options)

        # initializes an agent which allows us to call the relevant agent.
        self.agent = None

        # stores the trajectories of the agent/predator/prey
        self.agent_trajectories = []
        self.prey_trajectories = []
        self.predator_trajectories = [] 

    def step(self):
        """
        moves the agent, prey, and predator one step

        returns
        * 1 if agent wins
        * 0 if game in progress
        * -1 if agent looses 
        """
        self.agent.move(self.graph, self.prey, self.predator)
        self.agent_trajectories.append(self.agent.location)

        self.prey.move(self.graph)
        self.prey_trajectories.append(self.prey.location)
        if self.agent.location == self.prey.location:
            return 1

        self.predator.move(self.graph, self.agent)
        self.predator_trajectories.append(self.predator.location)
        if self.agent.location == self.predator.location:
            return -1

        return 0

    def step_debug(self):
        """
        moves the agent, prey, and predator one step

        returns
        * 1 if agent wins
        * 0 if game in progress
        * -1 if agent looses 
        """
        self.agent.move(self.graph, self.prey, self.predator)
        self.agent_trajectories.append(self.agent.location)

        self.prey.move_debug(self.graph)
        self.prey_trajectories.append(self.prey.location)
        if self.agent.location == self.prey.location:
            return 1

        self.predator.move_debug(self.graph, self.agent)
        self.predator_trajectories.append(self.predator.location)
        if self.agent.location == self.predator.location:
            return -1

        return 0

    def run_agent_1(self):
        self.agent = Agent1(self.agent_starting_location)

        status = 0
        while status == 0:
            status = self.step()

        return status

    def run_agent_1_debug(self):
        self.agent = Agent1(self.agent_starting_location)
        self.visualize_graph()

        status = 0
        while status == 0:
            status = self.step_debug()
            self.visualize_graph()

        return status

    def run_agent_2(self):
        self.agent = Agent2(self.agent_starting_location)

        status = 0
        while status == 0:
            status = self.step()

        return status

    def run_agent_2_debug(self):
        self.agent = Agent2(self.agent_starting_location)
        self.visualize_graph()

        status = 0
        while status == 0:
            status = self.step_debug()
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
        plt.rcParams['figure.figsize'] = [16, 8]
        G = nx.from_dict_of_lists(self.graph.get_neighbors())
        my_pos = nx.spring_layout(G, seed=100)
        nx.draw(G, pos=my_pos, node_color=self.visualize_graph_color_map(), with_labels=True)

        figure_text = "Agent: {}, Prey: {}, Predator: {}".format(self.agent.location, self.prey.location, self.predator.location)
        plt.figtext(0.5, 0.05, figure_text, ha="center", fontsize=10)

        trajectories = f"Agent: {self.agent_trajectories}\nPrey: {self.prey_trajectories}\nPredator: {self.predator_trajectories}"
        plt.figtext(0.1, 0.1, trajectories, ha="left", fontsize=8)

        plt.show()

    def visualize_graph_circle(self):
        """visualizes nodes and their edges with labels in a circular layout"""
        nx.draw_networkx(nx.Graph(self.graph.get_neighbors()), pos=nx.circular_layout(
            nx.Graph(self.graph.get_neighbors())), node_color=self.visualize_graph_color_map(), node_size=50, with_labels=True)
        plt.show()

    