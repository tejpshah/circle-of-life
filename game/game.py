import random
import networkx as nx
import matplotlib.pyplot as plt
from game.agents.agent1 import Agent1
from game.agents.agent2 import Agent2
from game.agents.agent3 import Agent3
from game.agents.agent4 import Agent4
from game.agents.agent5 import Agent5
from game.agents.agent6 import Agent6
from game.agents.agent7 import Agent7
from game.agents.agent8 import Agent8
from game.agents.agent7b import Agent7B
from game.agents.agent8b import Agent8B
from game.agents.agent7c import Agent7C
from game.agents.agent8c import Agent8C
from game.agents.agent9 import Agent9
from game.agents.agent10 import Agent10
from .graph import Graph
from .predator import Predator
from .predatored import PredatorED
from .prey import Prey


class Game:
    def __init__(self, nodes=50, timeout=1000):
        # initializes the graph on which agents/prey/predator play
        self.graph = Graph(nodes=nodes)

        # initializes prey location to be random from nodes 1...50
        self.prey = Prey(random.randint(1, self.graph.get_nodes()))

        # determines the predator location which will be used to create the specific predator
        self.predator = None
        self.predator_location = random.randint(1, self.graph.get_nodes())

        # agent initializes randomly to any spot that is not occupied by predator/prey
        occupied_s = min(self.prey.location, self.predator_location)
        occupied_l = max(self.prey.location, self.predator_location)
        agent_location_options = list(range(1, occupied_s)) + list(range(
            occupied_s+1, occupied_l)) + list(range(occupied_l+1, self.graph.get_nodes() + 1))
        self.agent_starting_location = random.choice(agent_location_options)

        # initializes an agent which allows us to call the relevant agent.
        self.agent = None

        # stores the trajectories of the agent/predator/prey
        self.agent_trajectories = [self.agent_starting_location]
        self.prey_trajectories = [self.prey.location]
        self.predator_trajectories = [self.predator_location]

        # initializes the number of steps before timing out
        self.timeout = timeout

        # initializes the number of steps the agent took
        self.steps = 0

    def step_return_values(self, status, found_prey, found_pred):
        """
        returns status & found_prey/found_pred as a percentage of total moves
        """
        if found_prey is not None and found_pred is not None:
            return status, found_prey/self.steps * 100, found_pred/self.steps * 100
        elif found_prey is not None:
            return status, found_prey/self.steps * 100, found_pred
        elif found_pred is not None:
            return status, found_prey, found_pred/self.steps * 100
        else:
            return status, found_prey, found_pred

    def step(self):
        """
        moves the agent, prey, and predator one step

        returns
        * 1 if agent wins
        * 0 if game in progress
        * -1 if agent looses 

        also returns number of times agent knew the exact location of the prey and the pred in the partial information settings
        """
        self.steps = self.steps + 1

        found_prey, found_pred = self.agent.move(
            self.graph, self.prey, self.predator)
        self.agent_trajectories.append(self.agent.location)
        if self.agent.location == self.prey.location:
            return self.step_return_values(1, found_prey, found_pred)
        if self.agent.location == self.predator.location:
            return self.step_return_values(-1, found_prey, found_pred)

        self.prey.move(self.graph)
        self.prey_trajectories.append(self.prey.location)
        if self.agent.location == self.prey.location:
            return self.step_return_values(1, found_prey, found_pred)

        self.predator.move(self.graph, self.agent)
        self.predator_trajectories.append(self.predator.location)
        if self.agent.location == self.predator.location:
            return self.step_return_values(-1, found_prey, found_pred)

        return self.step_return_values(0, found_prey, found_pred)

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
        found_prey, found_pred = self.agent.move_debug(
            self.graph, self.prey, self.predator)
        self.agent_trajectories.append(self.agent.location)
        if self.agent.location == self.prey.location:
            return 1, found_prey, found_pred
        if self.agent.location == self.predator.location:
            return -1, found_prey, found_pred

        self.prey.move(self.graph)
        self.prey_trajectories.append(self.prey.location)
        if self.agent.location == self.prey.location:
            return 1, found_prey, found_pred

        self.predator.move(self.graph, self.agent)
        self.predator_trajectories.append(self.predator.location)
        if self.agent.location == self.predator.location:
            return -1, found_prey, found_pred

        return 0, found_prey, found_pred

    def run_agent_1(self):
        self.predator = Predator(self.predator_location)
        self.agent = Agent1(self.agent_starting_location)

        status = 0
        step_count = 0

        while status == 0 and step_count < self.timeout:
            status, _, _ = self.step()
            step_count = step_count + 1

        # agent timed out
        if status == 0:
            status = -2

        return status

    def run_agent_1_debug(self):
        self.predator = Predator(self.predator_location)
        self.agent = Agent1(self.agent_starting_location)
        self.visualize_graph()

        status = 0
        step_count = 0

        while status == 0 and step_count < self.timeout:
            status, _, _ = self.step_debug()
            step_count = step_count + 1
            self.visualize_graph()

        self.visualize_graph_video()

        # agent timed out
        if status == 0:
            status = -2

        return status

    def run_agent_2(self):
        self.predator = Predator(self.predator_location)
        self.agent = Agent2(self.agent_starting_location)

        status = 0
        step_count = 0

        while status == 0 and step_count < self.timeout:
            status, _, _ = self.step()
            step_count = step_count + 1

        # agent timed out
        if status == 0:
            status = -2

        return status

    def run_agent_2_debug(self):
        self.predator = Predator(self.predator_location)
        self.agent = Agent2(self.agent_starting_location)
        self.visualize_graph()

        status = 0
        step_count = 0

        while status == 0 and step_count < self.timeout:
            status, _, _ = self.step_debug()
            step_count = step_count + 1
            self.visualize_graph()

        self.visualize_graph_video()

        # agent timed out
        if status == 0:
            status = -2

        return status

    def run_agent_3(self):
        self.predator = Predator(self.predator_location)
        self.agent = Agent3(self.agent_starting_location, self.graph)

        status = 0
        step_count = 0
        found_prey = 0

        while status == 0 and step_count < self.timeout:
            status, found_prey, _ = self.step()
            step_count = step_count + 1

        # agent timed out
        if status == 0:
            status = -2

        return status, found_prey

    def run_agent_3_debug(self):
        self.predator = Predator(self.predator_location)
        self.agent = Agent3(self.agent_starting_location, self.graph)
        status = 0
        step_count = 0
        found_prey = 0

        while status == 0 and step_count < self.timeout:
            status, found_prey, _ = self.step_debug()
            step_count = step_count + 1
            self.visualize_graph()

        self.visualize_graph_video()

        # agent timed out
        if status == 0:
            status = -2

        return status, found_prey

    def run_agent_4(self):
        self.predator = Predator(self.predator_location)
        self.agent = Agent4(self.agent_starting_location, self.graph)

        status = 0
        step_count = 0
        found_prey = 0

        while status == 0 and step_count < self.timeout:
            status, found_prey, _ = self.step()
            step_count = step_count + 1

        # agent timed out
        if status == 0:
            status = -2

        return status, found_prey

    def run_agent_4_debug(self):
        self.predator = Predator(self.predator_location)
        self.agent = Agent4(self.agent_starting_location, self.graph)

        status = 0
        step_count = 0
        found_prey = 0

        while status == 0 and step_count < self.timeout:
            status, found_prey, _ = self.step()
            step_count = step_count + 1
            self.visualize_graph()

        self.visualize_graph_video()

        # agent timed out
        if status == 0:
            status = -2

        return status, found_prey

    def run_agent_5(self):
        self.predator = PredatorED(self.predator_location)
        self.agent = Agent5(self.agent_starting_location,
                            self.graph, self.predator)

        status = 0
        step_count = 0
        found_pred = 0

        while status == 0 and step_count < self.timeout:
            status, _, found_pred = self.step()
            step_count = step_count + 1

        # agent timed out
        if status == 0:
            status = -2

        return status, found_pred

    def run_agent_5_debug(self):
        self.predator = PredatorED(self.predator_location)
        self.agent = Agent5(self.agent_starting_location,
                            self.graph, self.predator)

        status = 0
        step_count = 0
        found_pred = 0

        self.visualize_graph()

        while status == 0 and step_count < self.timeout:
            status, _, found_pred = self.step_debug()
            step_count = step_count + 1
            self.visualize_graph()

        self.visualize_graph_video()

        # agent timed out
        if status == 0:
            status = -2

        return status, found_pred

    def run_agent_6(self):
        self.predator = PredatorED(self.predator_location)
        self.agent = Agent6(self.agent_starting_location,
                            self.graph, self.predator)

        status = 0
        step_count = 0
        found_pred = 0

        while status == 0 and step_count < self.timeout:
            status, _, found_pred = self.step()
            step_count = step_count + 1

        # agent timed out
        if status == 0:
            status = -2

        return status, found_pred

    def run_agent_6_debug(self):
        self.predator = PredatorED(self.predator_location)
        self.agent = Agent6(self.agent_starting_location,
                            self.graph, self.predator)

        status = 0
        step_count = 0
        found_pred = 0

        self.visualize_graph()

        while status == 0 and step_count < self.timeout:
            status, _, found_pred = self.step_debug()
            step_count = step_count + 1
            self.visualize_graph()

        self.visualize_graph_video()

        # agent timed out
        if status == 0:
            status = -2

        return status, found_pred

    def run_agent_7(self):
        self.predator = PredatorED(self.predator_location)
        self.agent = Agent7(self.agent_starting_location,
                            self.graph, self.predator)

        status = 0
        step_count = 0
        found_pred = 0

        while status == 0 and step_count < self.timeout:
            status, found_prey, found_pred = self.step()
            step_count = step_count + 1

        # agent timed out
        if status == 0:
            status = -2

        return status, found_prey, found_pred

    def run_agent_7_debug(self):
        self.predator = PredatorED(self.predator_location)
        self.agent = Agent7(self.agent_starting_location,
                            self.graph, self.predator)

        status = 0
        step_count = 0
        found_pred = 0

        self.visualize_graph()

        while status == 0 and step_count < self.timeout:
            status, found_prey, found_pred = self.step_debug()
            step_count = step_count + 1
            self.visualize_graph()

        self.visualize_graph_video()

        # agent timed out
        if status == 0:
            status = -2

        return status, found_prey, found_pred

    def run_agent_8(self):
        self.predator = PredatorED(self.predator_location)
        self.agent = Agent8(self.agent_starting_location,
                            self.graph, self.predator)

        status = 0
        step_count = 0
        found_pred = 0

        while status == 0 and step_count < self.timeout:
            status, found_prey, found_pred = self.step()
            step_count = step_count + 1

        # agent timed out
        if status == 0:
            status = -2

        return status, found_prey, found_pred

    def run_agent_8_debug(self):
        self.predator = PredatorED(self.predator_location)
        self.agent = Agent8(self.agent_starting_location,
                            self.graph, self.predator)

        status = 0
        step_count = 0
        found_pred = 0

        self.visualize_graph()

        while status == 0 and step_count < self.timeout:
            status, found_prey, found_pred = self.step_debug()
            step_count = step_count + 1
            self.visualize_graph()

        self.visualize_graph_video()

        # agent timed out
        if status == 0:
            status = -2

        return status, found_prey, found_pred

    def run_agent_7B(self):
        self.predator = PredatorED(self.predator_location)
        self.agent = Agent7B(self.agent_starting_location,
                             self.graph, self.predator)

        status = 0
        step_count = 0
        found_pred = 0

        while status == 0 and step_count < self.timeout:
            status, found_prey, found_pred = self.step()
            step_count = step_count + 1

        # agent timed out
        if status == 0:
            status = -2

        return status, found_prey, found_pred

    def run_agent_7B_debug(self):
        self.predator = PredatorED(self.predator_location)
        self.agent = Agent7B(self.agent_starting_location,
                             self.graph, self.predator)

        status = 0
        step_count = 0
        found_pred = 0

        self.visualize_graph()

        while status == 0 and step_count < self.timeout:
            status, found_prey, found_pred = self.step_debug()
            step_count = step_count + 1
            self.visualize_graph()

        self.visualize_graph_video()

        # agent timed out
        if status == 0:
            status = -2

        return status, found_prey, found_pred

    def run_agent_8B(self):
        self.predator = PredatorED(self.predator_location)
        self.agent = Agent8B(self.agent_starting_location,
                             self.graph, self.predator)

        status = 0
        step_count = 0
        found_pred = 0

        while status == 0 and step_count < self.timeout:
            status, found_prey, found_pred = self.step()
            step_count = step_count + 1

        # agent timed out
        if status == 0:
            status = -2

        return status, found_prey, found_pred

    def run_agent_8B_debug(self):
        self.predator = PredatorED(self.predator_location)
        self.agent = Agent8B(self.agent_starting_location,
                             self.graph, self.predator)

        status = 0
        step_count = 0
        found_pred = 0

        self.visualize_graph()

        while status == 0 and step_count < self.timeout:
            status, found_prey, found_pred = self.step_debug()
            step_count = step_count + 1
            self.visualize_graph()

        self.visualize_graph_video()

        # agent timed out
        if status == 0:
            status = -2

        return status, found_prey, found_pred

    def run_agent_7C(self):
        self.predator = PredatorED(self.predator_location)
        self.agent = Agent7C(self.agent_starting_location,
                             self.graph, self.predator)

        status = 0
        step_count = 0
        found_pred = 0

        while status == 0 and step_count < self.timeout:
            status, found_prey, found_pred = self.step()
            step_count = step_count + 1

        # agent timed out
        if status == 0:
            status = -2

        return status, found_prey, found_pred

    def run_agent_7C_debug(self):
        self.predator = PredatorED(self.predator_location)
        self.agent = Agent7C(self.agent_starting_location,
                             self.graph, self.predator)

        status = 0
        step_count = 0
        found_pred = 0

        self.visualize_graph()

        while status == 0 and step_count < self.timeout:
            status, found_prey, found_pred = self.step_debug()
            step_count = step_count + 1
            self.visualize_graph()

        self.visualize_graph_video()

        # agent timed out
        if status == 0:
            status = -2

        return status, found_prey, found_pred

    def run_agent_8C(self):
        self.predator = PredatorED(self.predator_location)
        self.agent = Agent8C(self.agent_starting_location,
                             self.graph, self.predator)

        status = 0
        step_count = 0
        found_pred = 0

        while status == 0 and step_count < self.timeout:
            status, found_prey, found_pred = self.step()
            step_count = step_count + 1

        # agent timed out
        if status == 0:
            status = -2

        return status, found_prey, found_pred

    def run_agent_8C_debug(self):
        self.predator = PredatorED(self.predator_location)
        self.agent = Agent8C(self.agent_starting_location,
                             self.graph, self.predator)

        status = 0
        step_count = 0
        found_pred = 0

        self.visualize_graph()

        while status == 0 and step_count < self.timeout:
            status, found_prey, found_pred = self.step_debug()
            step_count = step_count + 1
            self.visualize_graph()

        self.visualize_graph_video()

        # agent timed out
        if status == 0:
            status = -2

        return status, found_prey, found_pred

    def run_agent_9(self):
        self.predator = PredatorED(self.predator_location)
        self.agent = Agent9(self.agent_starting_location,
                            self.graph, self.predator)

        status = 0
        step_count = 0
        found_pred = 0

        while status == 0 and step_count < self.timeout:
            status, found_prey, found_pred = self.step()
            step_count = step_count + 1

        # agent timed out
        if status == 0:
            status = -2

        return status, found_prey, found_pred

    def run_agent_9_debug(self):
        self.predator = PredatorED(self.predator_location)
        self.agent = Agent9(self.agent_starting_location,
                            self.graph, self.predator)

        status = 0
        step_count = 0
        found_pred = 0

        self.visualize_graph()

        while status == 0 and step_count < self.timeout:
            status, found_prey, found_pred = self.step_debug()
            step_count = step_count + 1
            self.visualize_graph()

        self.visualize_graph_video()

        # agent timed out
        if status == 0:
            status = -2

        return status, found_prey, found_pred

    def run_agent_10(self):
        self.predator = PredatorED(self.predator_location)
        self.agent = Agent10(self.agent_starting_location,
                             self.graph, self.predator)

        status = 0
        step_count = 0
        found_pred = 0

        while status == 0 and step_count < self.timeout:
            status, found_prey, found_pred = self.step()
            step_count = step_count + 1

        # agent timed out
        if status == 0:
            status = -2

        return status, found_prey, found_pred

    def run_agent_10_debug(self):
        self.predator = PredatorED(self.predator_location)
        self.agent = Agent10(self.agent_starting_location,
                             self.graph, self.predator)

        status = 0
        step_count = 0
        found_pred = 0

        self.visualize_graph()

        while status == 0 and step_count < self.timeout:
            status, found_prey, found_pred = self.step_debug()
            step_count = step_count + 1
            self.visualize_graph()

        self.visualize_graph_video()

        # agent timed out
        if status == 0:
            status = -2

        return status, found_prey, found_pred

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
