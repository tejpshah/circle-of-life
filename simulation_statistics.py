from game.game import Game


def agent1(num_simulations, nodes=50):
    """
    run simulation n times and get statistics on success
    """
    agent_success = []
    for _ in range(num_simulations):
        game = Game(nodes)
        game_success = game.run_agent_1()

        # agent caught the prey = 1, predator caught the agent = 0
        agent_success.append(1 if game_success == 1 else 0)

    wins = sum(agent_success)
    losses = len(agent_success) - wins
    success = wins/(wins + losses)
    print(
        f"Agent1: Wins: {wins}\tLosses: {losses}\tSuccess Rate: {round(success*100,2)}%")
    return round(success*100, 2)


def agent2(num_simulations, nodes=50):
    """
    run simulation n times and get statistics on success
    """
    agent_success = []
    for _ in range(num_simulations):
        game = Game(nodes)
        game_success = game.run_agent_2()

        # agent caught the prey = 1, predator caught the agent = 0
        agent_success.append(1 if game_success == 1 else 0)

    wins = sum(agent_success)
    losses = len(agent_success) - wins
    success = wins/(wins + losses)
    print(
        f"Agent2: Wins: {wins}\tLosses: {losses}\tSuccess Rate: {round(success*100,2)}%")
    return round(success*100, 2)

def agent3(num_simulations, nodes=50):
    """
    run simulation n times and get statistics on success
    """
    agent_success = []
    for _ in range(num_simulations):
        game = Game(nodes)
        game_success = game.run_agent_3()

        # agent caught the prey = 1, predator caught the agent = 0
        agent_success.append(1 if game_success == 1 else 0)

    wins = sum(agent_success)
    losses = len(agent_success) - wins
    success = wins/(wins + losses)
    print(
        f"Agent3: Wins: {wins}\tLosses: {losses}\tSuccess Rate: {round(success*100,2)}%")
    return round(success*100, 2)
