import numpy as np

def read_input(input_file_dir):
    """ 
    Parse reactor safety reports from the input file.

    Returns a 2D numpy array of reactor safety reports.
    """
    with open(input_file_dir, "r") as f:
        lines = f.readlines()
    
    array = []
    for line in lines:
        curr = np.fromstring(line, dtype=int, sep=' ')
        array.append(curr)
    
    return array


def is_report_safe(report):
    """ 
    Determine if a single reactor report is safe. 
    
    Returns 0 if the report is unsafe, 1 if the report is safe.
    """
    # if the report has only one number or no numbers, it is safe (considered sorted)
    if len(report) <= 1:
        return 1
    
    # Calculate differences between consecutive elements in each report
    diffs = np.diff(report)
    
    # Check if differences are consistently between 1 and 3 (ascending)
    # or between -3 and -1 (descending)
    return int(np.all((diffs >= 1) & (diffs <= 3)) or 
               np.all((diffs <= -1) & (diffs >= -3)))


def is_report_safe_with_dampener(report):
    """ 
    Check if a report is safe using the Problem Dampener. Tries to make the report safe by removing a single bad level.
    
    Returns 0 if the report is unsafe, 1 if the report is safe.
    """
    # First check if the report is safe without modifications
    if is_report_safe(report):
        return 1
    
    # Try removing each level to see if it becomes safe
    for level in range(len(report)):
        modified_report = np.delete(report, level)
        if is_report_safe(modified_report):
            return 1
    
    return 0


def count_safe_reports(reports, use_dampener=False):
    """ 
    Count the number of safe reports in a 2D array of reactor reports. Uses the Problem Dampener if specified.
    
    Returns the number of safe reports.
    """
    safety_check = is_report_safe_with_dampener if use_dampener else is_report_safe
    return np.sum(np.fromiter((safety_check(report) for report in reports), dtype=int))


if __name__ == "__main__":
    reports = read_input("input.txt")

    # part 1
    print(count_safe_reports(reports, use_dampener=False))

    # part 2
    print(count_safe_reports(reports, use_dampener=True))
