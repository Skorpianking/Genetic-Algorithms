# Genetic-Algorithms
Hosts GA files

22 June 16:  Added three intial Python files. circle_finder and expression_finder each use a simple GA to find possible answers to a trivial problem.  expression_finder takes a user number as input and then derives a mathematical expression that equals that number.  Since I limited to a set number of generations, a solution may not be found.  circle_finder attempts to find the largest circle that can be possibly drawn among other circles.  The circles cannot overlap or intersect in any way.  Again, it is limited to a set number of generations, so the size of the circle found may not be the largest possible.  circle_class is just that, a simple circle class used by circle_finder.

25 June 16:  Added knapsack.py.  Implements simple GA to find a solution (not guarenteed to be optimal) for the knapsack problem.  If given N items each with a specific value (V) and weight (W), find a combination of those items (each can only be selected once), that will not exceed the weight capacity of the knapsack yet maximize the value inside the knapsack.
