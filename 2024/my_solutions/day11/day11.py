from functools import cache 

def read_input(input_file_dir):
    """
    Load the initial configuration of Plutonian stones from a file. Each stone's engraving is represented as an integer.

    Returns a list of numerical values engraved on the stones in their original order.
    """
    with open(input_file_dir, 'r') as file:
        stones = [int(x) for x in file.readline().split()]

    return stones


def simulate_blinks(stones, blinks=25):
    """
    Process stones through multiple blinks, applying transformation rules.
    
    Returns the number of stones after specified blinks.
    """
    for _ in range(blinks):
        # Combine stone transformation logic directly in this function
        output = []
        for stone in stones:
            # Rule 1: If stone is 0, replace with 1
            if stone == 0:
                output.append(1)
                continue
            
            # Convert stone to string for digit manipulation
            string = str(stone)
            length = len(string)
            
            # Rule 2: If even number of digits, split into two stones
            if length % 2 == 0:
                output.append(int(string[:length // 2]))
                output.append(int(string[length // 2:]))
            else:
                # Rule 3: If no other rules apply, multiply by 2024
                output.append(stone * 2024)
        
        # Update stones for next iteration
        stones = output
    
    return len(stones)


@cache
def calc_stones_after_blinks(stone, blinks):
    """
    Recursively count stones for a single initial stone after specified steps (blinks). Uses memoization to optimize performance.
    
    Returns the number of stones after specified steps (blinks).
    """
    # Base case: if no steps left, return 1 stone
    if blinks == 0:
        return 1
    
    # Rule 1: If stone is 0, replace with 1
    if stone == 0:
        return calc_stones_after_blinks(1, blinks - 1)
    
    # Convert stone to string for digit manipulation
    string = str(stone)
    length = len(string)
    
    # Rule 2: If even number of digits, split into two stones
    if length % 2 == 0:
        return (
            calc_stones_after_blinks(int(string[:length // 2]), blinks - 1) + 
            calc_stones_after_blinks(int(string[length // 2:]), blinks - 1)
        )
    
    # Rule 3: If no other rules apply, multiply by 2024
    return calc_stones_after_blinks(stone * 2024, blinks - 1)


if __name__ == "__main__":
    stones = read_input("input.txt")

    # part 1
    print(simulate_blinks(stones)) # after 25 blinks

    # part 2
    print(sum(calc_stones_after_blinks(stone, 75) for stone in stones)) # after 75 blinks
