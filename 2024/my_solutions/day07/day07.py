def read_input(input_file_dir):
    """
    Read input equations from a text file.

    Returns a list of tuples, where each tuple contains a target number and an array of numbers.
    """
    equations = []
    with open(input_file_dir, 'r') as file:
        for line in file:
            # Split the line into target and array
            left, right = line.split(": ")
            target = int(left)
            array = [int(num) for num in right.split()]
            equations.append((int(target), array))
    
    return equations


def is_equation_solvable(target, array, allow_concatenation=False):
    """
    Recursively check if the target number can be obtained by applying multiplication, addition, or concatenation to the array of numbers.

    Returns True if the target number can be obtained using the array of numbers, False otherwise.
    """
    # base case for single element
    if len(array) == 1:
        return target == array[0]

    # recursive cases: try division and subtraction
    # MULTIPLICATION: divide the target by the last element
    if target % array[-1] == 0 and is_equation_solvable(target // array[-1], array[:-1], allow_concatenation):
        return True

    # ADDITION: subtract the last element from the target
    if target > array[-1] and is_equation_solvable(target - array[-1], array[:-1], allow_concatenation):
        return True

    # CONCATENATION: check if the target number can be obtained by concatenating the last element to the rest of the array
    if allow_concatenation:
        s_target = str(target)
        s_last = str(array[-1])
        if len(s_target) > len(s_last) and s_target.endswith(s_last) and is_equation_solvable(int(s_target[:-len(s_last)]), array[:-1], allow_concatenation):
            return True

    return False

    
def sum_solvable_equation_targets(equations, allow_concatenation=False):
    """
    Calculate the sum of target numbers that can be obtained by applying operators to their respective number arrays.

    Returns the sum of the target numbers that can be obtained.
    """
    total = 0

    for target, array in equations:
        if is_equation_solvable(target, array, allow_concatenation):
            total += target
    
    return total


if __name__ == "__main__":
    calibration_equations = read_input("input.txt")

    # part 1
    print(sum_solvable_equation_targets(calibration_equations, allow_concatenation=False))

    # part 2
    print(sum_solvable_equation_targets(calibration_equations, allow_concatenation=True))
