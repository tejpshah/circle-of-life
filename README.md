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
 