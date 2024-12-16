from collections import deque
from typing import List, Set, Tuple

def read_input(input_file_dir):
    """
    Reads the topographic map from the input file and converts it into a grid of integers.

    Returns A 2D list of integers representing the map.
    """
    with open(input_file_dir, 'r') as file:
        grid = [[int(char) for char in line.strip()] for line in file]

    return grid


def find_trailheads(grid):
    """
    Identifies all potential trailheads (positions with height 0) in the topographic grid.

    Returns A list of tuples (row, column) representing the positions of all trailheads.
    """
    rows = len(grid)
    cols = len(grid[0])
    return [(r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 0]


def evaluate_trailhead_potential(grid, row, column, mode="score"):
    """
    Evaluates a trailhead's potential based on different metrics of hiking trail exploration.

    Type of evaluation - 'score' or 'rating'.
        - 'score': Returns the number of height-9 positions reachable from the trailhead.
        - 'rating': Returns the number of distinct hiking trails beginning at the trailhead.

    Returns the trailhead's score or rating depending on the evaluation type.
    """
    rows = len(grid)
    cols = len(grid[0])

    q = deque([(row, column)])

    if mode == "score":
        seen = {(row, column)}
        summits = 0
        while len(q) > 0:
            cr, cc = q.popleft()
            for nr, nc in [(cr - 1, cc), (cr, cc + 1), (cr + 1, cc), (cr, cc - 1)]:
                if nr < 0 or nc < 0 or nr >= rows or nc >= cols: 
                    continue
                if grid[nr][nc] != grid[cr][cc] + 1: 
                    continue
                if (nr, nc) in seen: 
                    continue
                seen.add((nr, nc))
                if grid[nr][nc] == 9:
                    summits += 1
                else:
                    q.append((nr, nc))
        return summits

    elif mode == "rating":
        seen = {(row, column): 1}
        trails = 0
        while len(q) > 0:
            cr, cc = q.popleft()
            if grid[cr][cc] == 9:
                trails += seen[(cr, cc)]
            for nr, nc in [(cr - 1, cc), (cr, cc + 1), (cr + 1, cc), (cr, cc - 1)]:
                if nr < 0 or nc < 0 or nr >= rows or nc >= cols: 
                    continue
                if grid[nr][nc] != grid[cr][cc] + 1: 
                    continue
                if (nr, nc) in seen:
                    seen[(nr, nc)] += seen[(cr, cc)]
                    continue
                seen[(nr, nc)] = seen[(cr, cc)]
                q.append((nr, nc))
        return trails

    else:
        raise ValueError("invalid mode")


def calculate_total_score(grid, mode="score") -> int:
    """
    Calculates the total trailhead metric by summing up individual trailhead evaluations.

    Type of evaluation - 'score' or 'rating'.
        - 'score': Returns the number of height-9 positions reachable from the trailhead.
        - 'rating': Returns the number of distinct hiking trails beginning at the trailhead.
        
    Returns the total metric for all trailheads in the grid.
    """
    trailheads = find_trailheads(grid)
    return sum(evaluate_trailhead_potential(grid, r, c, mode) for r, c in trailheads)


if __name__ == "__main__":
    grid = read_input("input.txt")

    # part 1
    print(calculate_total_score(grid, "score"))

    # part 2
    print(calculate_total_score(grid, "rating"))
