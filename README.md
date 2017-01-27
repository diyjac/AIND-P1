# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: **Contraint Propagation** is a powerful technique used in AI.  It is all about using local constraints in a space to dramatically reduce the search space for solving a given problem.  For Sudoku, the constraints are the rules that a box can only have a single digit from 1 to 9 and the digits *must* only occur once in a given unit: 9 rows, 9 columns, 9 3x3 squares.  The naked twins technique is the following. Consider the following puzzle, and look at the two highlighted boxes, 'F3' and 'I3'.

![naked-twins](./images/naked-twins.png)

As we can see, both belong to the same column, and both permit the values of 2 and 3. Now, we don't know which one has a 2 and which one has a 3, but we know one thing for sure — the values 2 and 3 are locked in those two boxes, so no other box in their same unit (the third column) can contain the values 2 or 3.  So how can we use this constraint to our advantage?  We can remove all values 2 or 3 from boxes that are in units that belongs to the same units as those two squares!  This will further reduce our search space for solving our sudoku puzzle.  In this case, the squares D3 and E3 are good candidates to use in our search size reduction efforts.  So, by propagating this additional *naked-twins* constrain to the next iteration, we reduce our search size significantly, and may help solve sudoku puzzles that we were not able to before.

![naked-twins2](./images/naked-twins-2.png)

And here is the function we use to implement the *naked-twins* technique:

```
def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    ##########################################################################################################
    # we first find all possible naked twins values on the board
    # then we use those values and isolate only the ones that appears more than once on the boar: our candidates
    # with our candidates, we iterate through our unitlist and find units that have square with the candidate values
    # once we isolated the possible units with our candidate values, we get a list of all values for that unit
    # with the unit value list, we confirm our naked-twins by verifying that they occur more than once in a unit and add them to our list.
    # with the confirmed set of naked-twins, we search the units that have them and add them to a dictionary
    ##########################################################################################################

    all_possible_naked_twins_values = [values[box] for box in values.keys() if len(values[box]) == 2]
    candidate_naked_twins_values = [candidate for candidate in all_possible_naked_twins_values if all_possible_naked_twins_values.count(candidate)>1]
    units_with_candidates = [u for u in unitlist for candidate in candidate_naked_twins_values for s in u if values[s]==candidate]
    units_with_candidates_values_list = dict(("+".join(u), [values[s] for s in u]) for u in units_with_candidates)
    naked_twin_list = [twins for twins in candidate_naked_twins_values for u in units_with_candidates if units_with_candidates_values_list["+".join(u)].count(twins)>1]
    units_with_naked_twins = dict(("+".join(u),naked) for u in units_with_candidates for naked in naked_twin_list if units_with_candidates_values_list["+".join(u)].count(naked)>1)
   
    # Eliminate the naked twins as possibilities for their peers
    ##########################################################################################################
    # we already have the list of units and the naked-twins associated with them in our dictionary
    # we just need to iterate through them and for squares that are not the ones with the naked-twins values,
    # we remove the digits from them that are part of the naked-twins.  DONE!
    ##########################################################################################################
    for naked_unit in units_with_naked_twins.keys():
        naked = units_with_naked_twins[naked_unit]
        for box in naked_unit.split('+'):
            if values[box] != naked:
                for digit in naked:
                    values = assign_value(values, box, values[box].replace(digit,''))
    return values
```


# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?
A: A diagonal sudoku is like a regular sudoku, except that among the two main diagonals, the numbers 1 to 9 should all appear exactly once. In this project we will solve every diagonal sudoku too.  Below is a visualization of what this new diagonal sudoku additional constraints looks like:

![diagonal sudoku](./images/diagonal-sudoku.png)

As with before,  **Contraint Propagation** is a powerful technique used in AI.  It is all about using local constraints in a space to dramatically reduce the search space for solving a given problem.  For diagonal sudoku, we added two additional constraints that the numbers 1 to 9 can only appear once in the 2 diagonals units.  One would think that these additional constraints are an added burden, but on the contrary, these new constrainst actually simplifies the problem by reducing our search space for solving our sudoku puzzle even further!  The code segment below shows how we implemented the diagonal units into our agent:

```
## create our board and different views into the boards
## boxes
rows = 'ABCDEFGHI'
cols = '123456789'
...

###################################################################################################
# We are creating our diagonal units here...
###################################################################################################
colslist = list(cols)
colslist.reverse()
revcols = "".join(colslist)
diagonal_units = [[rs+cs for rs,cs in zip(rows,cols)], [rs+cs for rs,cs in zip(rows,revcols)]]
###################################################################################################
# Element example:
# diagonal_units[0] = ['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9']
# A diagonal sudoku is like a regular sudoku, except that among the two main diagonals,
#   the numbers 1 to 9 should all appear exactly once.
#   In this project, we will solve every diagonal sudoku.
###################################################################################################

# now a list of units
unitlist = row_units + column_units + square_units + diagonal_units
```

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

### Data

The data consists of a text file of diagonal sudokus for you to solve.

### Conclusion

This was a great project.  Have Fun!
