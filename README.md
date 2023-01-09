# Graduate AI Project 2: Circle-Of-Life
This project involves building a simulator for the "Circle-Of-Life" game and developing intelligent agents to play the game in complete information, partial prey, partial predator, complete partial, and complete partial defective environments. The project was completed in collaboration between Tej Shah and Srinandini Marpaka.

Lab Report: https://github.com/tejpshah/circle-of-life/blob/master/lab-report/tej-nandini-labreport2-final.pdf

Agent Video Simulations: https://github.com/tejpshah/circle-of-life/tree/master/videos

## Motivation
Uncertainty is a fundamental aspect of many real-world situations and can have a profound impact on the performance of intelligent agents. How do we deal with uncertainty when making decisions? How do we reason about the likelihood of different events occurring? How do we update our beliefs as new information becomes available? How do we evaluate the trade-offs between different outcomes and choose the best course of action? These are just some of the questions that we address in this module on uncertainty. Through this project, we delve into the concepts of probability, inference, Bayesian networks, and decision theory, and explore how these ideas can be applied to make intelligent agents that are capable of reasoning and acting under uncertainty. We examine how to build models of uncertain systems, how to make inferences based on these models, and how to use these inferences to guide decision-making over time. By studying these topics, we gain a deeper understanding of how to design intelligent agents that can adapt and thrive in uncertain environments.

## The Simulator
In the complete information and partial prey environments, the predator is optimal, always selecting actions that maximally decrease the distance to the agent from its action space. In all other environments, the predator is distracted, choosing optimal actions with a probability of 0.6 and a random neighbor with a probability of 0.4. The prey always selects any one of its neighbors or its current node randomly. There are 3 entities in the environment: the prey, the predator, and the agent. These 3 entities interact with each other on a graph environment with |V|=50 nodes. The agent moves first, then the prey, and then the predator. If the agent and prey occupy the same node, then the agent wins. If the agent and the predator occupy the same node, the predator wins. The game can terminate early after t time steps.

## The Agents
We develop $A1, A2, \ldots, A10$ in various environments: complete, partial prey, partial predator, complete partial, and complete partial defective. Odd numbered agents are specified according to the assignment description and even number agents are designed by us to out-perform the assignment specifications. For the interested reader, more information on each agent's strategy is detailed in the lab report. 

## Experimental Results
Even numbered agents of our own design outperform all specified odd numbered agents. For the interested reader, more information on experiments between agents in different settings of uncertainty are detailed in the lab report. 