import json
import os
import simulation_statistics as simulation_statistics


def save_simulation_statistics(setting, agent, success_rates):
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

    data[agent] = success_rates

    with open(filepath, "w") as fp:
        json.dump(data, fp)


def labreport_simulation_statistics_agent1():
    """
    runs 100 simulations 30 times and returns the average 
    """
    success_rates = []
    for _ in range(30):
        simulation_success = simulation_statistics.agent1(100, 50)
        success_rates.append(simulation_success)

    average = sum(success_rates) / len(success_rates)

    save_simulation_statistics("complete", "agent1", success_rates)
    print(
        f"Agent1: Overall Success Rate: {round(average,2)}%")
    return round(average, 2)


def labreport_simulation_statistics_agent2():
    """
    runs 100 simulations 30 times and returns the average 
    """
    success_rates = []
    for _ in range(30):
        simulation_success = simulation_statistics.agent2(100, 50)
        success_rates.append(simulation_success)

    average = sum(success_rates) / len(success_rates)

    save_simulation_statistics("complete", "agent2", success_rates)
    print(
        f"Agent2: Overall Success Rate: {round(average,2)}%")
    return round(average, 2)


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
    # labreport_simulation_statistics_agent1()
    # labreport_simulation_statistics_agent2()
    # simulation_statistics.visualize("data/", "simulation_statistics_complete.json")

    # labreport_simulation_statistics_agent3()
    # labreport_simulation_statistics_agent4()
    # simulation_statistics.visualize("data/", "simulation_statistics_partial-prey.json")

    simulation_statistics.agent3(1, 50)
