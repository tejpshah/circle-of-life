# circle-of-life-project2
 CS520 Project 2, Tej & Nandini

# OCTOBER 29th, 2022 NOTES -- ACTION ITEMS

## VERIFICATIONS & SANITY CHECKS & TESTING:
- @Nandini - Sanity check that A3 works and matches assignment specifications. Specifically, check belief updates, and make sure that they are working properly in each possible scenario. 
- @Nandini - Sanity check that A4 works and the logic looks reasonable. 
- @Nandini - Sanity check that A5 works and matches assignment specifications. Specifically, check belief updates, and make sure that they are working properly in each possible scenario. 
- @Nandini - Sanity check that A6 works and the logic looks reasonable. 
- @Nandini - Sanity check that A7 works and matches assignment specifications. Specifically, check belief updates, and make sure that they are working properly in each possible scenario. 
- @Nandini - Sanity check that A8 works and the logic looks reasonable. 
- @Nandini - Lab Report Read through Introduction and make sure it makes sense
- @Nandini - Lab Report Read through A1 and make sure it makes sense
- @Nandini - Lab Report Read through A2 and make sure it makes sense
- @Nandini - Lab Report Read through A3 and make sure it makes sense
- @Nandini - Lab Report Read through A4 and make sure it makes sense
- @Nandini - Lab Report Read through A5 and make sure it makes sense
- @Nandini - Lab Report Read through A6 and make sure it makes sense
- @Nandini - Lab Report Read through A7 and make sure it makes sense
- @Nandini - Lab Report Read through A8 and make sure it makes sense
- @Nandini - Lab Report Read through Lab Report Q3.1 and make sure it makes sense
- @Nandini - Lab Report Read through Lab Report Q3.2 and make sure it makes sense
- @Nandini - Lab Report Read through Lab Report Q3.3 and make sure it makes sense

## NEXT STEPS
- @Tej/Nandini: Implement A7 Defective Signal + Run Experiments. 
- @Tej/Nandini: Implement A8 Defective Signal + Run Experiments. 
- @Nandini: Implement A9 accounting for defective signal (this is tricky)
	- Potential Ideas: If two or three readings are close to each other for predator then we're good to go
	- Potential Ideas: Store copies of the current sensor readings and pick any one of its possible readings with highest probability
	- Potential Ideas: Update the beliefs according to Bayes Rule (given that the sensor is defective, you update all the belief rules)
	- Potential Ideas: https://pooyanjamshidi.github.io/csce580/project4/ as reference Q3
	- Potential Ideas: https://pooyanjamshidi.github.io/csce580/project4/ as reference Q8 (joint particle filtering)
	- Potential Ideas: https://core.ac.uk/download/pdf/188224232.pdf
-@Nandini Write up LaTeX information about A9. 
-@Nandini: Implement the bonus for when you can only move/signal. 
-@Nandini Write up LaTeX information about A10. 
-@Nandini Write up LaTeX Q3.4 explaining for each agent, strengths and drawbacks.
-@Nandini: Write up LaTeX Q3.5 bonus explanation. 
-@Nandini/Tej: Export all experiments and post all the diagrams/tables to LaTeX for the expimernatl results section.
-@Nandini - Write up the experimental results section talking about the performance in each of the environments and detailing experiments. 
-@Nandini/Tej - Write an automated script to generate a positive and failure case video for each agent. 


## Lab Report Q1.1 
We initialize the graph with 50 nodes. 
At each of the nodes, we have max degree of 3. 
So, maximum number of edges is 150*3=150 edges. 
But, with the initial circle we have 50*2=100 edges.
There are possible edges = 150 - 100 = 50 edges. 
But, each edge needs two nodes, so 50/2 = 25 max nodes

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

## Things To Discuss:
	⁃	Nandini / Tej - Set up the belief updates equation for A5 to send to Aravind, the component of how the predator changes, to Aravind. 
	⁃	Nandini / Tej - Write up core logic description for Agent 3 in the Lab Report. 
	⁃	Nandini / Tej  - Write up core logic description for Agent 4 in the Lab Report. 
	⁃	Nandini - can you add timeout functionality to all the games of t=500 time steps (Aravind said he might specify the amount late but let’s have functionality)? 
	⁃	Nandini - can you add functionality within the agents/game to store number of wins, number of losses, and number of hung simulations? 
	⁃	Nandini - can you add functionality to retrieve the number of times A3 knows exactly where the prey is and return that when computing simulation statistics? [need for all, return prey and pred]
	⁃	@Tej - can you write out belief updates using mathematical notation(especially the component on belief propagation) for A3/A5? 
	⁃	@Tej - write out mathematical belief propagation updates in Lab Report for A3. 
	⁃	@Tej - write out mathematical belief propagation updates in Lab Report for A5. 

