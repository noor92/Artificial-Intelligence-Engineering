# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Contraint Propogation is the method in which we try to assign values to variables to meet the conditions or contraints set. In the naked twins, the condition was that upon finding two squares that are the same, we would have to exclude the possibilities in other squares to contain those particular values.

In order to solve this, I went through all the units and found all the instances of the naked twins and their respective positions. Thus forming an object that contains all the naked twins instances such as [I1,I3] for example.
Once i had their posisitons, I found the common peers between them and iterated. If any of the other peers had those values I would remove those particular values.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: To solve this, I created two diagonal objects and added them to my unit list. This constraint consequently reduces the searching space.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).
### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the `assign_value` function provided in solution.py

