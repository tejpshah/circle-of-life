# circle-of-life-project
 CS520 Project 2, Tej & Nandini

## NEXT STEPS
- @Tej/Nandini: Implement A7 Defective Signal + Run Experiments. 
- @Tej/Nandini: Implement A8 Defective Signal + Run Experiments. 
- @Nandini: Implement A9 accounting for defective signal (this is tricky)
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

## Bayes 
Suppose that you have a graph with n=50 nodes. There is a predator at node_i. At every time step, we can survey one node to update the beliefs overall of the belief that the predator is at node_i. 

For the Combined Partial Information Setting:  imagine that your survey drone is defective, and that if somethingis actually occupying a node being surveyed, there is a 0.1 probability that it gets reported as unoccupied (a false negative).

P(signal = True | prey exists @ node_i) = 0.9
P(signal = False | prey exists @ node_i) = 0.1

P(signal = True | prey does not exist @ node_i) = 0.1
P(signal = False | prey does not exist @ node_i) = 0.9

P(prey exists @ node_I | signal = True)
P(prey exists @ node_I | signal = False)

P(prey exists @ node_I | signal = True) = P(signal = True | prey exists @ node_i) * P(prey exists @ node_i) / P(signal = True)
P(prey exists @ node_I | signal = False) = P(signal = False | prey exists @ node_i) * P(prey exists @ node_i) / P(signal = False)

P(prey exists @ node_I | signal = True) = 0.9 * P(prey exists @ node_i) / P(signal = True)
P(prey exists @ node_I | signal = False) = 0.1 * P(prey exists @ node_i) / P(signal = False)

P(prey exists @ node_I | signal = True) = 0.9 * P(prey exists @ node_i) / (0.9 * P(prey exists @ node_i) + 0.1 * P(prey does not exist @ node_i))
P(prey exists @ node_I | signal = False) = 0.1 * P(prey exists @ node_i) / (0.1 * P(prey exists @ node_i) + 0.9 * P(prey does not exist @ node_i))