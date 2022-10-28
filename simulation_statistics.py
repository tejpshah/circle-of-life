import json
import os
import matplotlib.pyplot as plt
import numpy as np
from game.game import Game


def agent1(num_simulations, nodes=50):
    """
    run simulation n times and get statistics on success
    """
    agent_success = []
    timeouts = 0
    for _ in range(num_simulations):
        game = Game(nodes)
        game_success = game.run_agent_1()

        # agent caught the prey = 1, predator caught the agent/timeout = 0
        agent_success.append(1 if game_success == 1 else 0)

        # timeout if game_success returns -2
        timeouts = timeouts + 1 if game_success == -2 else timeouts

    wins = sum(agent_success)
    losses = len(agent_success) - wins - timeouts
    success = wins/(len(agent_success))
    print(
        f"Agent1: Wins: {wins}\tLosses: {losses}\tTimeouts: {timeouts}\tSuccess Rate: {round(success*100,2)}%")
    return wins, losses, timeouts, round(success*100, 2)


def agent2(num_simulations, nodes=50):
    """
    run simulation n times and get statistics on success
    """
    agent_success = []
    timeouts = 0
    for _ in range(num_simulations):
        game = Game(nodes)
        game_success = game.run_agent_2()

        # agent caught the prey = 1, predator caught the agent/timeout = 0
        agent_success.append(1 if game_success == 1 else 0)

        # timeout if game_success returns -2
        timeouts = timeouts + 1 if game_success == -2 else timeouts

    wins = sum(agent_success)
    losses = len(agent_success) - wins - timeouts
    success = wins/(len(agent_success))
    print(
        f"Agent2: Wins: {wins}\tLosses: {losses}\tTimeouts: {timeouts}\tSuccess Rate: {round(success*100,2)}%")
    return wins, losses, timeouts, round(success*100, 2)


def agent3(num_simulations, nodes=50):
    """
    run simulation n times and get statistics on success
    """
    agent_success = []
    timeouts = 0
    found_prey = 0
    for _ in range(num_simulations):
        game = Game(nodes)
        game_success, game_found_prey = game.run_agent_3()

        # agent caught the prey = 1, predator caught the agent/timeout = 0
        agent_success.append(1 if game_success == 1 else 0)

        # timeout if game_success returns -2
        timeouts = timeouts + 1 if game_success == -2 else timeouts

        # stores how often the agent knew where the prey was
        found_prey = found_prey + game_found_prey

    wins = sum(agent_success)
    losses = len(agent_success) - wins - timeouts
    success = wins/(len(agent_success))
    print(
        f"Agent3: Wins: {wins}\tLosses: {losses}\tTimeouts: {timeouts}\tSuccess Rate: {round(success*100,2)}%")
    return wins, losses, timeouts, round(success*100, 2), found_prey/num_simulations


def agent4(num_simulations, nodes=50):
    """
    run simulation n times and get statistics on success
    """
    agent_success = []
    timeouts = 0
    found_prey = 0
    for _ in range(num_simulations):
        game = Game(nodes)
        game_success, game_found_prey = game.run_agent_4()

        # agent caught the prey = 1, predator caught the agent/timeout = 0
        agent_success.append(1 if game_success == 1 else 0)

        # timeout if game_success returns -2
        timeouts = timeouts + 1 if game_success == -2 else timeouts

        # stores how often the agent knew where the prey was
        found_prey = found_prey + game_found_prey

    wins = sum(agent_success)
    losses = len(agent_success) - wins - timeouts
    success = wins/(len(agent_success))
    print(
        f"Agent4: Wins: {wins}\tLosses: {losses}\tTimeouts: {timeouts}\tSuccess Rate: {round(success*100,2)}%")
    return wins, losses, timeouts, round(success*100, 2), found_prey/num_simulations

def agent5(num_simulations, nodes=50):
    """
    run simulation n times and get statistics on success
    """
    agent_success = []
    timeouts = 0
    found_pred = 0
    for _ in range(num_simulations):
        game = Game(nodes)
        game_success, game_found_pred = game.run_agent_5()

        # agent caught the prey = 1, predator caught the agent/timeout = 0
        agent_success.append(1 if game_success == 1 else 0)

        # timeout if game_success returns -2
        timeouts = timeouts + 1 if game_success == -2 else timeouts

        # stores how often the agent knew where the prey was
        found_pred = found_pred + game_found_pred

    wins = sum(agent_success)
    losses = len(agent_success) - wins - timeouts
    success = wins/(len(agent_success))
    print(
        f"Agent5: Wins: {wins}\tLosses: {losses}\tTimeouts: {timeouts}\tSuccess Rate: {round(success*100,2)}%")
    return wins, losses, timeouts, round(success*100, 2), found_pred/num_simulations

def agent6(num_simulations, nodes=50):
    """
    run simulation n times and get statistics on success
    """
    agent_success = []
    timeouts = 0
    found_prey = 0
    for _ in range(num_simulations):
        game = Game(nodes)
        game_success, game_found_prey = game.run_agent_6()

        # agent caught the prey = 1, predator caught the agent/timeout = 0
        agent_success.append(1 if game_success == 1 else 0)

        # timeout if game_success returns -2
        timeouts = timeouts + 1 if game_success == -2 else timeouts

        # stores how often the agent knew where the prey was
        found_prey = found_prey + game_found_prey

    wins = sum(agent_success)
    losses = len(agent_success) - wins - timeouts
    success = wins/(len(agent_success))
    print(
        f"Agent6: Wins: {wins}\tLosses: {losses}\tTimeouts: {timeouts}\tSuccess Rate: {round(success*100,2)}%")
    return wins, losses, timeouts, round(success*100, 2), found_prey/num_simulations

def visualize(dirname, filename):
    """
    plot the simulation success rates and error bars
    """
    # get the agent setting
    setting = filename[:-5].split("_")[-1]

    # read the file
    filepath = dirname + filename
    with open(filepath, 'r') as fp:
        data = json.load(fp)

    # get the mean and standard deviation of each agent
    agents = []
    means = []
    stds = []
    for agent, value in data.items():
        agents.append(f'{agent[:-1].capitalize()} {agent[-1]}')
        success_rates = value['success-rates']
        np_success_rates = np.array(success_rates)
        means.append(np.mean(np_success_rates))
        stds.append(2 * np.std(np_success_rates))  # 2 standard deviations

    # create the bar graph with error bars
    x_pos = np.arange(len(agents))
    colors = ["lightcoral", "yellowgreen"]

    _, axes = plt.subplots()
    axes.bar(x_pos, means, color=colors, yerr=stds,
             align='center', ecolor='black', capsize=10)

    plt.title(f'{setting.title()} Agents\' Average Success Rates')
    axes.set_xticks(x_pos)
    axes.set_xticklabels(agents)
    plt.gca().set_ylim(bottom=0, top=100)
    plt.ylabel('Success Rate (%)')

    # save the bar graph
    if not os.path.exists(os.path.dirname(dirname)):
        os.makedirs(os.path.dirname(dirname))

    plot_name = "{}visualize_statistics_{}.png".format(dirname, setting)
    plt.savefig(plot_name, bbox_inches='tight')

    # show the bar graph
    # plt.show()

    return 1


#game = Game()
#game.run_agent_6_debug()
