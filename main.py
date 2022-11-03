import json
import os
import simulation_statistics as simulation_statistics


def get_overall_simulation_statistics(wins, losses, timeouts, success_rates, found_prey=None, found_pred=None):
    average_wins = round(sum(wins) / len(wins), 2)
    average_losses = round(sum(losses) / len(losses), 2)
    average_timeouts = round(sum(timeouts) / len(timeouts), 2)
    average_success = round(sum(success_rates) / len(success_rates), 2)

    average_found_prey = round(
        sum(found_prey) / len(found_prey), 2) if found_prey != None else None
    average_found_pred = round(
        sum(found_pred) / len(found_pred), 2) if found_pred != None else None

    statistics = {"avg-wins": average_wins, "avg-losses": average_losses,
                  "avg-timeouts": average_timeouts, "avg-found-prey": average_found_prey,
                  "avg-found-pred": average_found_pred, "avg-success-rates": average_success}

    return {"overall": statistics, "success-rates": success_rates}


def save_simulation_statistics(setting, agent, agent_data):
    """
    stores overall statistics to a json file depending on agent setting
    settings are "complete", "partial-prey", "partial-pred", "combined-partial"
    """
    dirname = "data/"
    if not os.path.exists(os.path.dirname(dirname)):
        os.makedirs(os.path.dirname(dirname))

    filename = f'simulation_statistics_{setting}.json'
    filepath = dirname + filename
    if os.path.exists(filepath):
        with open(filepath, "r") as fp:
            data = json.load(fp)
    else:
        data = {}

    data[agent] = agent_data

    with open(filepath, "w") as fp:
        json.dump(data, fp)


def labreport_simulation_statistics_agent1():
    """
    runs 100 simulations 30 times and returns the average 
    """
    wins = []
    losses = []
    timeouts = []
    success_rates = []

    for _ in range(30):
        simulation_wins, simulation_losses, simulation_timeouts, simulation_success = simulation_statistics.agent1(
            100, 50)

        wins.append(simulation_wins)
        losses.append(simulation_losses)
        timeouts.append(simulation_timeouts)
        success_rates.append(simulation_success)

    agent_data = get_overall_simulation_statistics(
        wins, losses, timeouts, success_rates)
    save_simulation_statistics("complete", "agent1", agent_data)

    print(
        f"Agent1: Overall Success Rate: {round(sum(success_rates) / len(success_rates),2)}%")


def labreport_simulation_statistics_agent2():
    """
    runs 100 simulations 30 times and returns the average 
    """
    wins = []
    losses = []
    timeouts = []
    success_rates = []

    for _ in range(30):
        simulation_wins, simulation_losses, simulation_timeouts, simulation_success = simulation_statistics.agent2(
            100, 50)

        wins.append(simulation_wins)
        losses.append(simulation_losses)
        timeouts.append(simulation_timeouts)
        success_rates.append(simulation_success)

    agent_data = get_overall_simulation_statistics(
        wins, losses, timeouts, success_rates)
    save_simulation_statistics("complete", "agent2", agent_data)

    print(
        f"Agent2: Overall Success Rate: {round(sum(success_rates) / len(success_rates),2)}%")


def labreport_simulation_statistics_agent3():
    """
    runs 100 simulations 30 times and returns the average 
    """
    wins = []
    losses = []
    timeouts = []
    success_rates = []
    found_prey = []

    for _ in range(30):
        simulation_wins, simulation_losses, simulation_timeouts, simulation_success, simulation_found_prey = simulation_statistics.agent3(
            100, 50)

        wins.append(simulation_wins)
        losses.append(simulation_losses)
        timeouts.append(simulation_timeouts)
        success_rates.append(simulation_success)
        found_prey.append(simulation_found_prey)

    agent_data = get_overall_simulation_statistics(
        wins, losses, timeouts, success_rates, found_prey=found_prey)
    save_simulation_statistics("partial-prey", "agent3", agent_data)

    print(
        f"Agent3: Overall Success Rate: {round(sum(success_rates) / len(success_rates),2)}%")


def labreport_simulation_statistics_agent4():
    """
    runs 100 simulations 30 times and returns the average 
    """
    wins = []
    losses = []
    timeouts = []
    success_rates = []
    found_prey = []

    for _ in range(30):
        simulation_wins, simulation_losses, simulation_timeouts, simulation_success, simulation_found_prey = simulation_statistics.agent4(
            100, 50)

        wins.append(simulation_wins)
        losses.append(simulation_losses)
        timeouts.append(simulation_timeouts)
        success_rates.append(simulation_success)
        found_prey.append(simulation_found_prey)

    agent_data = get_overall_simulation_statistics(
        wins, losses, timeouts, success_rates, found_prey=found_prey)
    save_simulation_statistics("partial-prey", "agent4", agent_data)

    print(
        f"Agent4: Overall Success Rate: {round(sum(success_rates) / len(success_rates),2)}%")


def labreport_simulation_statistics_agent5():
    """
    runs 100 simulations 30 times and returns the average 
    """
    wins = []
    losses = []
    timeouts = []
    success_rates = []
    found_pred = []

    for _ in range(30):
        simulation_wins, simulation_losses, simulation_timeouts, simulation_success, simulation_found_pred = simulation_statistics.agent5(
            100, 50)

        wins.append(simulation_wins)
        losses.append(simulation_losses)
        timeouts.append(simulation_timeouts)
        success_rates.append(simulation_success)
        found_pred.append(simulation_found_pred)

    agent_data = get_overall_simulation_statistics(
        wins, losses, timeouts, success_rates, found_pred=found_pred)
    save_simulation_statistics("partial-predator", "agent5", agent_data)

    print(
        f"Agent5: Overall Success Rate: {round(sum(success_rates) / len(success_rates),2)}%")


def labreport_simulation_statistics_agent6():
    """
    runs 100 simulations 30 times and returns the average 
    """
    wins = []
    losses = []
    timeouts = []
    success_rates = []
    found_pred = []

    for _ in range(30):
        simulation_wins, simulation_losses, simulation_timeouts, simulation_success, simulation_found_pred = simulation_statistics.agent6(
            100, 50)

        wins.append(simulation_wins)
        losses.append(simulation_losses)
        timeouts.append(simulation_timeouts)
        success_rates.append(simulation_success)
        found_pred.append(simulation_found_pred)

    agent_data = get_overall_simulation_statistics(
        wins, losses, timeouts, success_rates, found_pred=found_pred)
    save_simulation_statistics("partial-predator", "agent6", agent_data)

    print(
        f"Agent6: Overall Success Rate: {round(sum(success_rates) / len(success_rates),2)}%")


def labreport_simulation_statistics_agent7():
    """
    runs 100 simulations 30 times and returns the average 
    """
    wins = []
    losses = []
    timeouts = []
    success_rates = []
    found_prey = []
    found_pred = []

    for _ in range(30):
        simulation_wins, simulation_losses, simulation_timeouts, simulation_success, simulation_found_prey, simulation_found_pred = simulation_statistics.agent7(
            100, 50)

        wins.append(simulation_wins)
        losses.append(simulation_losses)
        timeouts.append(simulation_timeouts)
        success_rates.append(simulation_success)
        found_prey.append(simulation_found_prey)
        found_pred.append(simulation_found_pred)

    agent_data = get_overall_simulation_statistics(
        wins, losses, timeouts, success_rates, found_prey=found_prey, found_pred=found_pred)
    save_simulation_statistics(
        "combined-partial-information", "agent7", agent_data)

    print(
        f"Agent7: Overall Success Rate: {round(sum(success_rates) / len(success_rates),2)}%")


def labreport_simulation_statistics_agent8():
    """
    runs 100 simulations 30 times and returns the average 
    """
    wins = []
    losses = []
    timeouts = []
    success_rates = []
    found_prey = []
    found_pred = []

    for _ in range(30):
        simulation_wins, simulation_losses, simulation_timeouts, simulation_success, simulation_found_prey, simulation_found_pred = simulation_statistics.agent8(
            100, 50)

        wins.append(simulation_wins)
        losses.append(simulation_losses)
        timeouts.append(simulation_timeouts)
        success_rates.append(simulation_success)
        found_prey.append(simulation_found_prey)
        found_pred.append(simulation_found_pred)

    agent_data = get_overall_simulation_statistics(
        wins, losses, timeouts, success_rates, found_prey=found_prey, found_pred=found_pred)
    save_simulation_statistics(
        "combined-partial-information", "agent8", agent_data)

    print(
        f"Agent8: Overall Success Rate: {round(sum(success_rates) / len(success_rates),2)}%")


if __name__ == "__main__":
    # labreport_simulation_statistics_agent1()
    # labreport_simulation_statistics_agent2()
    simulation_statistics.visualize("data/", "simulation_statistics_complete.json")

    # labreport_simulation_statistics_agent3()
    # labreport_simulation_statistics_agent4()
    simulation_statistics.visualize("data/", "simulation_statistics_partial-prey.json")

    # labreport_simulation_statistics_agent5()
    # labreport_simulation_statistics_agent6()
    # simulation_statistics.visualize(
    #     "data/", "simulation_statistics_partial-predator.json")

    # labreport_simulation_statistics_agent7()
    # labreport_simulation_statistics_agent8()
    # simulation_statistics.visualize(
    #     "data/", "simulation_statistics_combined-partial-information.json")