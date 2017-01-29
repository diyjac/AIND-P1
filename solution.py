#!/usr/bin/python
"""
solution.py: version 0.1.0

This is the final code for creating an AI agent to solve all sudoku puzzles,
We implemented elimination, only choice, tree search and "naked twins" statagies and
enchanced the solver to solve diagonal sudoku as well.

History:
JAC: 2017/01/27: Initial version.
"""

assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    ##########################################################################################################
    # NOTE: we are using the same coding style as the AIND course materials to match, but are staging it to be
    #       more readable, with longer variable names.
    ##########################################################################################################

    # we first find all possible naked twins values on the board
    all_possible_naked_twins_values = [values[box] for box in values.keys()
                                       if len(values[box]) == 2]

    # then we use those values and isolate only the ones that appears more than once on the board: our candidates
    candidate_naked_twins_values = [candidate for candidate in all_possible_naked_twins_values
                                    if all_possible_naked_twins_values.count(candidate)>1]

    # with our candidates, we iterate through our unitlist and find units that have square with the candidate values
    units_with_candidates = [u for u in unitlist for candidate in candidate_naked_twins_values for s in u
                             if values[s]==candidate]

    # once we isolated the possible units with our candidate values, we get a list of all values for that unit
    units_with_candidates_values_list = dict(("+".join(u), [values[s] for s in u]) for u in units_with_candidates)

    # with the unit value list, we confirm our naked-twins by verifying that they occur more than once in a unit and add them to our list.
    naked_twin_list = [twins for twins in candidate_naked_twins_values for u in units_with_candidates
                       if units_with_candidates_values_list["+".join(u)].count(twins)>1] 

    # with the confirmed set of naked-twins, we search the units that have them and add them to a dictionary
    units_with_naked_twins = dict(("+".join(u),naked) for u in units_with_candidates for naked in naked_twin_list
                                   if units_with_candidates_values_list["+".join(u)].count(naked)>1)
    
    # Eliminate the naked twins as possibilities for their peers
    # we already have the list of units and the naked-twins associated with them in our dictionary
    for naked_unit in units_with_naked_twins.keys():
        naked = units_with_naked_twins[naked_unit]

        # we just need to iterate through them and for squares that are not the ones with the naked-twins values,
        for box in naked_unit.split('+'):

            # if the boxes are not part of the naked-twins.
            if values[box] != naked:
                for digit in naked:
                    # remove the digits from boxes that are not part of the naked-twins.  DONE!
                    values = assign_value(values, box, values[box].replace(digit,''))
    return values

## our helper function to create cross products
def cross(A, B):
    """Cross product of elements in A and elements in B."""
    return [s+t for s in A for t in B]

## create our board and different views into the boards
## boxes
rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)

# and units: row_units, column_units, square_units
row_units = [cross(r, cols) for r in rows]
# Element example:
# row_units[0] = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9']
# This is the top most row.

column_units = [cross(rows, c) for c in cols]
# Element example:
# column_units[0] = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1']
# This is the left most column.

square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
# Element example:
# square_units[0] = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']
# This is the top left square.

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

# create dictionaries
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
traversed = dict((s, False) for s in boxes)

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    board = dict(((boxes[i], grid[i]) for i in range(len(grid))))
    for box in board:
        if board[box] == '.':
            board[box] = '123456789'
    return board

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values = assign_value(values, peer, values[peer].replace(digit,''))
    return values


def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    new_values = values.copy()  # note: do not modify original values
    for unit in unitlist:
        for digit in '123456789':
            digitlist = []
            for box in unit:
                if digit in values[box]:
                    digitlist.append(box)
            if len(digitlist) == 1:
                new_values = assign_value(new_values, digitlist[0], digit)
    return new_values


def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # use eliminate, only_choice, naked_twins to try to solve the puzzle.
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    # "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function

    values = reduce_puzzle(values)
    if values is False:
        return False
    if len([box for box in boxes if len(values[box])==1]) == 81:
        # we are done
        return values

    # Choose one of the unfilled squares with the fewest possibilities
    n, box = min((len(values[box]), box) for box in boxes if len(values[box]) > 1)

    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for digit in values[box]:
        new_values = values.copy()
        #print("setting digit", digit, "for", box)
        new_values = assign_value(new_values, box, digit)
        attempt = search(new_values)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
