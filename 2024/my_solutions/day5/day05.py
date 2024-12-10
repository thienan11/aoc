import functools

def read_input(input_file_dir):
    """
    Parse the input text to extract page ordering rules and update lists.

    Returns a tuple of two lists:
    - The first list contains the ordering rules as pairs of page numbers.
    - The second list contains the update lists as lists of page numbers.
    """
    with open(input_file_dir, 'r') as file:
        file_contents = file.read()
    
    # Split input into rules and updates
    sections = file_contents.strip().split('\n\n')
    
    # Parse ordering rules
    rules = []
    for line in sections[0].split('\n'):
        if line.isspace():
            break
        rules.append(list(map(int, line.split("|"))))
    
    # Parse updates
    updates = [list(map(int, line.split(','))) for line in sections[1].split('\n')]
    
    return rules, updates


def is_valid_order(update, rules):
    """
    Check if an update list respects the ordering rules.

    Returns True if the update list is valid, False otherwise.
    """
    cache = {}
    for x, y in rules:
        cache[(x, y)] = True
        cache[(y, x)] = False

    # Check if the update respects all applicable rules
    for i in range(len(update)):
        for j in range(i + 1, len(update)):

            # Check if the rule is applicable
            key = (update[i], update[j])
            if key in cache and not cache[key]:
                # If the rule is violated, return False
                return False

    return True


def reorder_update(update, rules):
    """
    Sort an update list using custom comparison based on rules.

    The function constructs a directed graph of dependencies from the rules
    and uses it to define a custom comparison function for sorting.
    
    Returns a new list with the elements sorted according to the rules.
    """
    # Create a directed graph of dependencies
    dependencies = {}
    for x, y in rules:
        if x not in dependencies:
            dependencies[x] = set()
        dependencies[x].add(y)
    
    def comparator(a, b):
        """
        Compare two pages based on the rules.
        
        Returns:
        - Negative if a must come before b
        - Positive if b must come before a
        - 0 if no specific ordering rule exists
        """
        # Check if there's a direct rule
        if a in dependencies and b in dependencies[a]:
            return -1  # a must come before b
        if b in dependencies and a in dependencies[b]:
            return 1   # b must come before a
        return 0       # no specific ordering

    # Use Python's built-in sorting with custom comparison
    return sorted(update, key=functools.cmp_to_key(comparator))


def calc_middle_pages(rules, updates, process_valid_updates=True):
    """
    Calculate the sum of middle pages of all updates that respect the ordering rules.

    process_valid_updates (bool): 
        - True: Only consider correctly ordered updates (Part 1)
        - False: Only consider incorrectly ordered updates and reorder them before processing (Part 2)
    """
    total = 0
    
    # Check each update
    for update in updates:

        # Check if the update's order matches the desired condition
        is_currently_valid = is_valid_order(update, rules)
        
        # Determine if we should process this update
        if is_currently_valid == process_valid_updates:
            # If processing incorrectly ordered updates, reorder
            if not process_valid_updates:
                update = reorder_update(update, rules)
            
            # Find middle page
            middle_index = len(update) // 2
            total += update[middle_index]
    
    return total


if __name__ == "__main__":
    rules, updates = read_input("input.txt")

    # part 1
    print(calc_middle_pages(rules, updates))

    # part 2
    print(calc_middle_pages(rules, updates, process_valid_updates=False))
