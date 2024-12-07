def read_input(input_file_dir):
    """ Read the input file and return two lists of integers """
    list1 = []
    list2 = []

    with open(input_file_dir, "r") as f:
        for line in f:
            parts = line.strip().split()
            
            list1.append(int(parts[0]))
            list2.append(int(parts[1]))
    
    return list1, list2


def calculate_total_distance(list1, list2):
    """ Calculate the total distance between two lists of integers """
    list1.sort()
    list2.sort()
    total_distance = 0
    for i in range(len(list1)):
        total_distance += abs(list1[i] - list2[i])
    return total_distance


def calculate_similarity_score(list1, list2):
    """ Calculate the similarity score between two lists of integers """
    occurences = {}
    similarity_score = 0

    for num in list1:
        if num not in occurences:
            occurences[num] = 1
        else:
            curr_count = occurences[num]
            occurences[num] = curr_count + 1

    for num in list2:
        if num in occurences:
            count = num * occurences[num]
            similarity_score += count
    
    return similarity_score


if __name__ == "__main__":
    list1, list2 = read_input("input.txt")

    # part 1
    print(calculate_total_distance(list1, list2))

    # part 2
    print(calculate_similarity_score(list1, list2))
