# CSCI561
Artificial Intelligence assignments

Assignment and implementation details

1) An optimization version of n-queen's problem : Place officers in a nXn grid such that the total cost is maximized.
-> Used a combination of greedy and adversarial search with some pruning for optimization.
   Start with the highest cost cell and place an officer. Go to the next highest cost cell and try to see if there can be   
   collision. If not, place another officer and repeat until all p officers are placed without any collision. If there is no
   such possibility, backtrack and try with the next highest cost cell.
   Used DFS for search and pruned nodes based on the maximum possible cost by choosing a path.

2) A non zero sum minimax problem to solve the assignment of parking lot space and a bed in shelter for the homeless in LA
-> Applied non zero sum version of minimax algorithm for selecting the best candidate for a player. In the non-zero sum 
   version, we let the opponent play optimally first and then select the one option among those which has maximum utility.
   (Let the opponent choose the best option - Run minimax for the opponent and get plausible options that maximize opponent's
   utilities. Among these options, select the option that gives us the maximum utility)
   
   Exhaustive search for maximum utility. 
   Applied a greedy approach that runs faster for special inputs and run exhaustive search approach for other inputs for which
   the greedy algorithm gives a suboptimal solution.
   
3) A reinforcement learning algorithm application for self driving cars : Find the path to goal with maximum returns.
-> Application of Markov decision process to find the best policy. Used value iteration algorithm with the reduced weight in 
   order to get rid of the infinite horizon problem. After finding the best policy, I simulated the taxi driving from point A
   to point B(destination) and noted the total reward. 
