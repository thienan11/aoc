import regex as re

def read_input(input_file_dir):
    """ Parse memory instructions from the input file. """
    with open(input_file_dir, "r") as f:
        lines = f.read()

    return lines


def sum_multiplications(memory):
    """ 
    Extract and sum the results of valid multiplication instructions from corrupted memory.

    Returns the total sum of all valid multiplication results.

    Regex Pattern Details:
    - `mul\s*\(`: Matches 'mul' with optional whitespace before opening parenthesis
    - `(\d{1,3})`: Captures 1-3 digit numbers
    - `\s*,\s*`: Allows whitespace around the comma
    - `\s*\)`: Allows whitespace before closing parenthesis
    """
    # Use regex to find valid mul instructions
    pattern = r"mul\s*\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\)"
    # pattern = r"mul\((\d{1,3}),(\d{1,3})\)"

    # Find all matches
    memory_string = ''.join(memory) # Convert list of strings to single string
    matches = re.findall(pattern, memory_string)
    
    # Calculate and sum the results of valid mul instructions
    total = sum(int(x) * int(y) for x, y in matches)
    
    return total


def remove_inactive_memory(memory):
    """
    Filter out multiplication instructions based on the 'do()' and 'don't()' activation rules.

    Returns a list of memory segments that are active for multiplication, with each segment truncated at the first 'don't()' instruction.
    """
    filtered_memory = list()
    for element in memory.split("do()"):
        filtered_memory.append(element.split("don't()")[0])
    return filtered_memory


def sum_active_multiplications(memory):
    """
    Calculate the sum of multiplications for only the active instructions.
    """
    filtered_memory = remove_inactive_memory(memory)
    return sum_multiplications(filtered_memory)


if __name__ == "__main__":
    memory = read_input("input.txt")

    # part 1
    print(sum_multiplications(memory))

    # part 2
    print(sum_active_multiplications(memory))
