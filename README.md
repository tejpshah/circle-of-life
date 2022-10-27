# circle-of-life-project2
 CS520 Project 2, Tej & Nandini

## Lab Report Q1.1 
We initialize the graph with 50 nodes. 
At each of the nodes, we have max degree of 3. 
So, maximum number of edges is 150*3=150 edges. 
But, with the initial circle we have 50*2=100 edges.
There are possible edges = 150 - 100 = 50 edges. 
But, each edge needs two nodes, so 50/2 = 25 max nodes

# October 18th, 2022 Notes
- Environment is done completely.
- Prey, Predator, and the Agent is pretty much done, but may need to adjust based on functionality. 
- Agent 1: Pretty straightforward - needs to understand directions - hardcoded rules (<60 minutes)
- Agent 2: Predict optimal action for predator and prey, minimize pred first, max prey second
- Agent 3: 

- Add statistic on number of times where agent is seen and number of timesteps in the agent
-

# Tej's Working Session October 2019, 2022
- Sanity Check Complete: The implementation of graph is working as specified according to the writeup. 
- Sanity Check Complete: The implementation of prey is working as specified according to the writeup. 
- Sanity Check Complete: BFS in predator had exponential space time complexity. I made space complexity linear and stores previous pointers too.
- Sanity Check Complete: The game class looks good. Added extra functionality for debugging which stores the trajectories on the screen plus made game window bigger.
- Sanity Check Complete: The agent class looks good. Updated the BFS method with the more optimal BFS method from the Predator class. 
 
## Agent 3 and Agent 4
- Define a normalize method for the probability in both agent 3 and agent 4C

 ## Agent 4
 - Instead of choosing random.choice() for highest probability node, choose the node farthest from predator
 - Run Agent 2 instead of Agent 1 in super().move() 

 # Things To Discuss:
	⁃	Nandini / Tej - Set up the belief updates equation for A5 to send to Aravind, the component of how the predator changes, to Aravind. 
	⁃	Nandini / Tej - Write up core logic description for Agent 3 in the Lab Report. 
	⁃	Nandini / Tej  - Write up core logic description for Agent 4 in the Lab Report. 
	⁃	Nandini - can you add timeout functionality to all the games of t=500 time steps (Aravind said he might specify the amount late but let’s have functionality)? 
	⁃	Nandini - can you add functionality within the agents/game to store number of wins, number of losses, and number of hung simulations? 
	⁃	Nandini - can you add functionality to retrieve the number of times A3 knows exactly where the prey is and return that when computing simulation statistics? [need for all, return prey and pred]
	⁃	@Tej - can you write out belief updates using mathematical notation(especially the component on belief propagation) for A3/A5? 
	⁃	@Tej - write out mathematical belief propagation updates in Lab Report for A3. 
	⁃	@Tej - write out mathematical belief propagation updates in Lab Report for A5. 

