def read_input(input_file_dir):
    """
    Read the input grid and extract antenna positions organized by their frequency.

    Returns a tuple containing:
        - grid (list): A list of strings representing the grid rows
        - antennas (dict): A dictionary mapping frequencies to their antenna positions
    """
    with open(input_file_dir, 'r') as file:
        grid = [line.strip() for line in file]
    
    antennas = {}
    for r, row in enumerate(grid):
        for c, char in enumerate(row):
            if char != ".":
                if char not in antennas:
                    antennas[char] = []
                antennas[char].append((r, c))

    return grid, antennas


def calculate_antinodes(grid, antennas, include_antenna_positions=False):
    """
    Calculate antinodes based on antenna positions and the specified calculation method.

    Returns a set of unique antinode positions.
    """
    rows, cols = len(grid), len(grid[0])
    antinodes = set()
    for array in antennas.values():
        for i in range(len(array)):
            
            # Part 1: Only when one point is twice as far as the other
            if not include_antenna_positions:
                for j in range(i + 1, len(array)):
                    r1, c1 = array[i]
                    r2, c2 = array[j]
                    antinodes.add((2 * r1 - r2, 2 * c1 - c2))
                    antinodes.add((2 * r2 - r1, 2 * c2 - c1))

            # Part 2: Any line through two points of same frequency
            if include_antenna_positions:
                for j in range(len(array)):
                    if i == j: 
                        continue
                    r1, c1 = array[i]
                    r2, c2 = array[j]
                    dr = r2 - r1
                    dc = c2 - c1
                    r = r1
                    c = c1
                    while 0 <= r < rows and 0 <= c < cols:
                        antinodes.add((r, c))
                        r += dr
                        c += dc

    return antinodes


def count_valid_antinodes(grid, antinodes):
    """
    Count the number of antinodes that fall within the grid's boundaries.

    Returns the number of valid antinodes within the grid bounds.
    """
    rows, cols = len(grid), len(grid[0])
    return len([0 for r, c in antinodes if 0 <= r < rows and 0 <= c < cols])


if __name__ == "__main__":
    grid, antennas = read_input("input.txt")

    # part 1
    part1_antinodes = calculate_antinodes(grid, antennas, include_antenna_positions=False)
    print(count_valid_antinodes(grid, part1_antinodes))

    # part 2
    part2_antinodes = calculate_antinodes(grid, antennas, include_antenna_positions=True)
    print(count_valid_antinodes(grid, part2_antinodes))
