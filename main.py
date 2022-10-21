import simulation_statistics as simulation_statistics

def labreport_simulation_statistics_agent1():
    success_rates = []
    for _ in range(30):
        simulation_success = simulation_statistics.agent1(100, 50)
        success_rates.append(simulation_success)

    average = sum(success_rates) / len(success_rates)
    print(
        f"Agent1: Overall Success Rate: {round(average,2)}%")
    return round(average, 2)


def labreport_simulation_statistics_agent2():
    success_rates = []
    for _ in range(30):
        simulation_success = simulation_statistics.agent2(100, 50)
        success_rates.append(simulation_success)

    average = sum(success_rates) / len(success_rates)
    print(
        f"Agent2: Overall Success Rate: {round(average,2)}%")
    return round(average, 2)


if __name__ == "__main__":
    # simulation_statistics_agent1(10000)
    # labreport_simulation_statistics_agent1()
    # simulation_statistics_agent2(50)

    simulation_statistics.agent3(1, 10)
