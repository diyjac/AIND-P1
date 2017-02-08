# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

AIND-P1 is a *project result submission* for Udacity Diagonal Sudoku Solver project.  It is a command line python program with an optional pygame interface, in which we will use **elimination**, **only choice**, **naked-twin** and **search tree** techniques with **constraint propagation** AI stratagy to solve the sudoku puzzle in all its forms including the diagonal sudoku with its new diagonal units **A1 B2 C3 D4 E5 F6 G7 H8 I9** and **A9 B8 C7 D6 E5 F4 G3 H2 I1**.  The code that implements the additional **diagonal constraints** is located in [solution.py](./solution.py).   More details about this diagonal sudoku solver implementation can be found [here](./README-DETAILED.md)

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see our visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - This code implements our solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize the solution, we only assign values to the values_dict using the ```assign_values``` function provided in solution.py.  This will allow us to see and track the AI agents behavior when solving the sudoku puzzle:

![Pygame Window](./images/Screenshot from 2017-01-27 10-26-54.png)

## Contributing

No futher updates nor contributions are requested.  This project is static.

## License

AIND-P1 results are released under [MIT License](./LICENSE)

