import random
import networkx as nx
import matplotlib.pyplot as plt
from game.agents.agent1 import Agent1
from game.agents.agent2 import Agent2
from game.agents.agent3 import Agent3
from game.agents.agent4 import Agent4
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
        agent_location_options = list(range(1, occupied_s)) + list(range(
            occupied_s+1, occupied_l)) + list(range(occupied_l+1, self.graph.get_nodes() + 1))
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
        if self.agent.location == self.prey.location:
            return 1
        if self.agent.location == self.predator.location:
            return -1

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
        -- debug method --
        moves the agent, prey, and predator one step

        returns
        * 1 if agent wins
        * 0 if game in progress
        * -1 if agent looses 
        """
        print(f"THE NEIGHBORS ARE{self.graph.nbrs}")
        self.agent.move_debug(self.graph, self.prey, self.predator)
        self.agent_trajectories.append(self.agent.location)
        if self.agent.location == self.prey.location:
            return 1
        if self.agent.location == self.predator.location:
            return -1

        self.prey.move(self.graph)
        self.prey_trajectories.append(self.prey.location)
        if self.agent.location == self.prey.location:
            return 1

        self.predator.move(self.graph, self.agent)
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

        self.visualize_graph_video()
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

        self.visualize_graph_video()
        return status

    def run_agent_3(self):
        self.agent = Agent3(self.agent_starting_location, self.graph)
        status = 0
        while status == 0:
            status = self.step()

        return status

    def run_agent_3_debug(self):
        self.agent = Agent3(self.agent_starting_location, self.graph)
        status = 0
        while status == 0:
            status = self.step_debug()
            self.visualize_graph()

        self.visualize_graph_video()
        return status

    def run_agent_4(self):
        self.agent = Agent4(self.agent_starting_location, self.graph)
        status = 0
        while status == 0:
            status = self.step()

        return status

    def run_agent_4_debug(self):
        self.agent = Agent4(self.agent_starting_location, self.graph)
        status = 0
        while status == 0:
            status = self.step()
            self.visualize_graph()

        self.visualize_graph_video()
        return status

    def visualize_graph_color_map(self):
        """
        grey: unoccupied node
        green: node of prey 
        yellow: node of agent 
        pink: node of prey 
        """
        color_map = ["grey" for _ in self.graph.get_neighbors()]
        color_map[self.prey.location - 1] = "yellowgreen"
        color_map[self.predator.location - 1] = "lightcoral"

        if self.agent is not None:
            color_map[self.agent.location - 1] = "gold"

        return color_map

    def visualize_graph(self, fn='environment.png'):
        """visualizes nodes and their edges with labels in non-circular layout"""
        plt.rcParams['figure.figsize'] = [8, 6]
        G = nx.from_dict_of_lists(self.graph.get_neighbors())
        my_pos = nx.spring_layout(G, seed=100)
        nx.draw(G, pos=my_pos,
                node_color=self.visualize_graph_color_map(), with_labels=True)

        figure_text = "Agent: {}, Prey: {}, Predator: {}".format(
            self.agent.location, self.prey.location, self.predator.location)
        plt.figtext(0.5, 0.05, figure_text, ha="center", fontsize=10)

        trajectories = f"Agent: {self.agent_trajectories}\nPrey: {self.prey_trajectories}\nPredator: {self.predator_trajectories}"
        plt.figtext(0.1, 0.1, trajectories, ha="left", fontsize=8)

        plt.show()

    def visualize_graph_video(self, fn='videos/environment.mp4'):
        """visualizes nodes and their edges with labels in non-circular layout as a video"""
        import os
        plt.rcParams['figure.figsize'] = [16, 10]

        if os.path.exists(fn):
            os.remove(fn)

        G = nx.from_dict_of_lists(self.graph.get_neighbors())
        my_pos = nx.spring_layout(G, seed=100)

        for i in range(len(self.agent_trajectories)):
            plt.clf()  # make sure we clear any old stuff
            agent_location = self.agent_trajectories[min(
                i, len(self.agent_trajectories)-1)]
            prey_location = self.prey_trajectories[min(
                i, len(self.prey_trajectories)-1)]
            predator_location = self.predator_trajectories[min(
                i, len(self.predator_trajectories)-1)]

            color_map = ["grey" for _ in self.graph.get_neighbors()]
            color_map[prey_location - 1] = "yellowgreen"
            color_map[predator_location - 1] = "lightcoral"
            color_map[agent_location - 1] = "gold"

            nx.draw(G, pos=my_pos, node_color=color_map, with_labels=True)

            figure_text = "Agent: {}, Prey: {}, Predator: {}".format(
                agent_location, prey_location, predator_location)
            plt.figtext(0.5, 0.05, figure_text, ha="center", fontsize=10)

            plt.savefig('figure' + str(i) + '.png')  # save this figure to disk

        # now combine all of the figures into a video
        os.system('ffmpeg -r 3 -i figure%d.png -vcodec mpeg4 -y '+fn)
        print("A video showing the agent's traversal is ready to view. Opening...")
        os.system('open '+fn)

        # clean up the environment a bit
        for i in range(len(self.agent_trajectories)):
            os.remove('figure' + str(i) + '.png')

    def visualize_graph_circle(self):
        """visualizes nodes and their edges with labels in a circular layout"""
        nx.draw_networkx(nx.Graph(self.graph.get_neighbors()), pos=nx.circular_layout(
            nx.Graph(self.graph.get_neighbors())), node_color=self.visualize_graph_color_map(), node_size=50, with_labels=True)
        plt.show()
