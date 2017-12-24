assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    return [s+t for s in a for t in b]

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

#setting  diagonal units 
diagonal_units1=[[rows[i]+cols[i] for i in range(len(rows))]]
diagonal_units2=[[rows[i]+cols[-i-1] for i in range(len(rows))]]

unitlist = row_units + column_units + square_units + diagonal_units1 + diagonal_units2

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

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
    twin_instances = [box for box in values.keys() if len(values[box]) == 2]

    #Finding the positions of all the naked_twins
    #contains two items [I1, I3]
    twins_list =[[pos1,pos2] \
    for pos1 in twin_instances\
        for pos2 in peers[pos1]\
            if (values[pos1]) == (values[pos2])] #if the values are the same set them to the naked_twins lisst

    #getting positions
    for i in range(len(twins_list)):
        pos1 = twins_list[i][0]
        pos2 = twins_list[i][1]

        #finding common peers amongest the positions
        common_peers=(peers[pos1]) & (peers[pos2])

        #settimg values to related peers only 
        for peer in common_peers:
            if (len(values[peer])>1):
                for digit in values[pos1]:
                    values = assign_value(values,peer,values[peer].replace(digit,''))
    # print(values)
    return values



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
    newGrid = []
    digits='123456789'
    for item in grid:
        if item==".":
            newGrid.append(digits)
        elif item in digits:
            newGrid.append(item)
            
    assert len(newGrid) ==  81
    return dict(zip(boxes,newGrid))  



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
    solved_values = [key for key in values.keys() if len(values[key]) == 1]
    for key in solved_values:
        digit=values[key]
        for peer in peers[key]:
            values[peer]=values[peer].replace(digit,'')
         
    return values



def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            position= [box for box in unit if digit in values[box]]
            
            if len(position) == 1:
                values[position[0]] = digit
    return values



def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values=eliminate(values)

        values=naked_twins(values)


        # Your code here: Use the Only Choice Strategy
        values=only_choice(values)


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
    values= reduce_puzzle(values)
    if values is False:
        return False
        
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved, this only happens when it's actualy solved!


    # Choose one of the unfilled squares with the fewest possibilities
    #s prints g2 at the start 
    n,s=min((len(values[s]),s) for s in boxes if (len(values[s]))>1)
    
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for value in values[s]:
        newPuzzle=values.copy()
        newPuzzle[s]=value
        attempt= search(newPuzzle)
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

    #converting the grid to a dictionary 
    values = grid_values(grid)

    #calling search to solve the puzzle 
    solved = search(values)

    if solved:
        return solved
    else:
        return False

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
