def read_input(input_file_dir):
    """
    Read the input map from a text file.

    Returns a list of lists representing the map, where each inner list is a row of the map.
    """
    with open(input_file_dir, 'r') as file:
        file_contents = file.read().splitlines()
    
    grid = list(map(list, file_contents))

    return grid


def calculate_guard_visited_positions(grid):
    """
    Simulates the movement of a guard on a grid and calculates the number of unique positions 
    visited by the guard before they leave the map.

    Returns the number of unique positions visited by the guard.
    """
    rows, cols = len(grid), len(grid[0])

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "^":
                break
        else:
            continue
        break
    
    # Since guard is moving up:
    dr = -1 # decreasing row
    dc = 0 # constant column

    visited = set() # set of positions visited by the guard

    # Simulate the guard's movement until their next position is invalid
    while True:
        visited.add((r, c))
        if r + dr < 0 or r + dr >= rows or c + dc < 0 or c + dc >= cols: # guard is about to step out of position
            break

        if grid[r + dr][c + dc] == "#": # guard is about to hit a wall
            # move guard right
            dr, dc = dc, -dr
        else: # guard is about to move to an empty position
            # move guard forward
            r += dr
            c += dc

    return len(visited) # number of unique positions visited by the guard


def detect_loop(grid, start_r, start_c, start_dr, start_dc):
    """
    Detect if placing an obstruction at a specific position would cause the guard to enter a loop.

    Returns True if a loop is detected, False otherwise.
    """
    rows, cols = len(grid), len(grid[0])
    visited_states = set()  # to track (row, col, direction)

    r, c, dr, dc = start_r, start_c, start_dr, start_dc

    while True:
        state = (r, c, dr, dc)
        if state in visited_states:
            # if the current state is already visited, a loop is detected
            return True
        visited_states.add(state)

        # simulate guard movement
        next_r, next_c = r + dr, c + dc

        if next_r < 0 or next_r >= rows or next_c < 0 or next_c >= cols:
            # guard is about to leave the grid
            return False

        if grid[next_r][next_c] == "#":
            # guard hits an obstruction and turns right
            dr, dc = dc, -dr
        else:
            # move forward
            r, c = next_r, next_c


def find_obstruction_positions(grid):
    """
    Find all positions where placing an obstruction would cause the guard to enter a loop.

    Returns the number of valid positions.
    """
    rows, cols = len(grid), len(grid[0])

    # locate the guard's initial position and direction
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "^":
                start_r, start_c, start_dr, start_dc = r, c, -1, 0
                break
        else:
            continue
        break

    valid_positions = []

    # brute force: try placing an obstruction at every empty position (except the guard's starting position)
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "." and (r, c) != (start_r, start_c):
                # create a temporary grid with the obstruction
                grid[r][c] = "#"
                if detect_loop(grid, start_r, start_c, start_dr, start_dc):
                    valid_positions.append((r, c))
                # remove the obstruction after testing
                grid[r][c] = "."

    return len(valid_positions)


if __name__ == "__main__":
    grid = read_input('input.txt')

    # part 1
    print(calculate_guard_visited_positions(grid))

    # part 2
    print(find_obstruction_positions(grid)) # brute force solution
