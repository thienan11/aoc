def read_input(input_file_dir):
    """
    Reads the map of garden plots from the input file and converts it into a grid of characters.

    Returns A 2D list of characters representing the garden plots.
    """
    with open(input_file_dir, 'r') as file:
        grid = [list(line.strip()) for line in file]

    return grid


def find_regions(grid):
    """
    Find all contiguous regions of the same plant type in the grid.
    
    Returns a list of sets, where each set contains coordinates of a region
    """
    rows, cols = len(grid), len(grid[0])
    regions = []
    seen = set()
    
    for r in range(rows):
        for c in range(cols):
            # Skip if this cell has already been processed
            if (r, c) in seen:
                continue
            
            # Start a new region
            region = {(r, c)}
            seen.add((r, c))
            
            # Use BFS to find all connected cells of the same crop
            queue = [(r, c)]
            crop = grid[r][c]
            
            while queue:
                cr, cc = queue.pop(0)
                
                # Check all 4 adjacent cells
                for nr, nc in [(cr-1, cc), (cr+1, cc), (cr, cc-1), (cr, cc+1)]:
                    # Boundary and type checks
                    if (0 <= nr < rows and 0 <= nc < cols and 
                        grid[nr][nc] == crop and (nr, nc) not in region):
                        region.add((nr, nc))
                        queue.append((nr, nc))
            
            seen.update(region)
            regions.append(region)
    
    return regions


def calculate_region_perimeter(region):
    """
    Calculate the perimeter of a region (a set of coordinates). A side is counted if it does not touch another cell in the same region.
    
    Returns the perimeter of the region
    """
    perimeter_count = 0
    
    for (r, c) in region:
        # Start with 4 sides
        perimeter_count += 4
        
        # Subtract sides that touch other cells in the same region
        for nr, nc in [(r+1, c), (r-1, c), (r, c-1), (r, c+1)]:
            if (nr, nc) in region:
                perimeter_count -= 1
    
    return perimeter_count


def count_sides(region):
    """
    Count the number of sides in a region (set of coordinates) using a more complex algorithm. 
    This method counts the corner configurations to determine the number of sides.
    
    Returns the number of sides in the region.
    """
    # Generate corner candidates around the region
    corner_candidates = set()
    for r, c in region:
        for cr, cc in [(r - 0.5, c - 0.5), (r + 0.5, c - 0.5), 
                       (r + 0.5, c + 0.5), (r - 0.5, c + 0.5)]:
            corner_candidates.add((cr, cc))
    
    # Count the number of sides
    sides = 0
    for cr, cc in corner_candidates:
        # Check the configuration of surrounding cells
        config = [(sr, sc) in region for sr, sc in [
            (cr - 0.5, cc - 0.5), 
            (cr + 0.5, cc - 0.5), 
            (cr + 0.5, cc + 0.5), 
            (cr - 0.5, cc + 0.5)
        ]]
        
        # Count sides based on corner configuration
        number = sum(config)
        
        if number == 1:
            # Single cell corner
            sides += 1
        elif number == 2:
            # Handle specific two-cell configurations
            if config == [True, False, True, False] or config == [False, True, False, True]:
                sides += 2
        elif number == 3:
            # Three-cell configuration
            sides += 1
    
    return sides


if __name__ == "__main__":
    grid_garden_plots = read_input("input.txt")
    regions = find_regions(grid_garden_plots)

    # part 1
    # The total price of fencing regions using area × perimeter
    print(sum(len(region) * calculate_region_perimeter(region) for region in regions))

    # part 2
    # The total price using area × sides (multiplies region area by number of sides instead of perimeter)
    print(sum(len(region) * count_sides(region) for region in regions))
