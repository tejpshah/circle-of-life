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
    success_rates = []
    for _ in range(30):
        simulation_success = simulation_statistics.agent3(100, 50)
        success_rates.append(simulation_success)

    average = sum(success_rates) / len(success_rates)

    save_simulation_statistics("partial-prey", "agent3", success_rates)
    print(
        f"Agent3: Overall Success Rate: {round(average,2)}%")
    return round(average, 2)


def labreport_simulation_statistics_agent4():
    """
    runs 100 simulations 30 times and returns the average 
    """
    success_rates = []
    for _ in range(30):
        simulation_success = simulation_statistics.agent4(100, 50)
        success_rates.append(simulation_success)

    average = sum(success_rates) / len(success_rates)

    save_simulation_statistics("partial-prey", "agent4", success_rates)
    print(
        f"Agent4: Overall Success Rate: {round(average,2)}%")
    return round(average, 2)


if __name__ == "__main__":
    labreport_simulation_statistics_agent1()
    labreport_simulation_statistics_agent2()
    # simulation_statistics.visualize(
    #     "data/", "simulation_statistics_complete.json")

    # labreport_simulation_statistics_agent3()
    # labreport_simulation_statistics_agent4()
    # simulation_statistics.visualize("data/", "simulation_statistics_partial-prey.json")
