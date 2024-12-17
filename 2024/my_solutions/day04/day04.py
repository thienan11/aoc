def read_input(input_file_dir):
    """ 
    Read a grid of characters from a text file.

    Returns a list of lists, where each inner list represents a row of characters.
    """
    with open(input_file_dir, 'r') as f:
        # Read the content of the file, and split into lines
        grid = f.read().splitlines()
    return grid


def find_occurrences(grid, mode="XMAS"):
    """
    Find occurrences in the grid.
    Modes:
    - "XMAS": Find all occurrences of 'XMAS' in any orientation.
    - "X-MAS": Find all 'X-MAS' patterns (two MAS or SAM forming an X).
    """
    rows, cols = len(grid), len(grid[0])
    total_occurrences = 0

    # Mode: "XMAS" - Find all occurrences of 'XMAS' in any direction
    if mode == "XMAS":
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] != "X": # Skip if the character is not 'X'
                    continue

                # Check all possible directions (diagonal, vertical, and horizontal)
                for dr in [-1, 0, 1]: # Direction for rows: -1 (up), 0 (same row), 1 (down)
                    for dc in [-1, 0, 1]: # Direction for columns: -1 (left), 0 (same column), 1 (right)
                        if dr == dc == 0: # Skip the direction where both dr and dc are 0 (no movement)
                            continue

                        # Ensure the next coordinates are within bounds
                        if not (0 <= r + 3 * dr < len(grid) and 0 <= c + 3 * dc < len(grid[0])): 
                            continue

                        # Check if the pattern 'XMAS' exists in this direction
                        if grid[r + dr][c + dc] == "M" and grid[r + 2 * dr][c + 2 * dc] == "A" and grid[r + 3 * dr][c + 3 * dc] == "S":
                            total_occurrences += 1                   

    # Mode: "X-MAS" - Find all 'X-MAS' patterns (two MAS or SAM forming an X)
    elif mode == "X-MAS":
        for r in range(1, rows - 1):  # Exclude the first and last row to avoid out-of-bounds
            for c in range(1, cols - 1):  # Exclude the first and last column
                if grid[r][c] != "A": # Skip if the character is not 'A'
                    continue

                # Check the four corners around the 'A'
                corners = [grid[r - 1][c - 1], grid[r - 1][c + 1], grid[r + 1][c + 1], grid[r + 1][c - 1]]

                # If the corners match one of the valid X-MAS patterns, increment the occurrence count
                if "".join(corners) in ["MMSS", "MSSM", "SSMM", "SMMS"]:
                    total_occurrences += 1

    return total_occurrences


if __name__ == "__main__":
    word_search = read_input("input.txt")

    # part 1
    part_1_result = find_occurrences(word_search, mode="XMAS")
    print(f"Total 'XMAS' occurrences: {part_1_result}")

    # part 2
    part_2_result = find_occurrences(word_search, mode="X-MAS")
    print(f"Total 'X-MAS' occurrences: {part_2_result}")
