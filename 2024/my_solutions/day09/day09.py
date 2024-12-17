def read_input_p1(input_file_dir):
    """
    Parse the disk map from an input file into a list of file blocks and free spaces.

    Returns a list representing the disk, where file blocks are identified by their file ID, and free spaces are marked with -1
    """
    with open(input_file_dir, 'r') as file:
        data = file.read()
    
    disk = []
    fid = 0

    # process each character in the input
    for i, char in enumerate(data):
        block_size = int(char)

        # even indices represent file blocks, odd indices represent free spaces
        if i % 2 == 0:
            # add file blocks with sequential file IDs
            disk += [fid] * block_size
            fid += 1
        else:
            # add free space blocks marked as -1
            disk += [-1] * block_size
    
    return disk


def read_input_p2(input_file_dir):
    """
    Parse the disk map into files and blank spaces.

    Returns:
        dict: A dictionary of files, where the keys are file IDs and the values are tuples (start_position, size/length).
        list: A list of tuples representing free spaces, where each tuple is (start_position, size).
        int: The total number of files.
    """
    with open(input_file_dir, 'r') as file:
        data = file.read()
    
    files = {}
    blanks = []

    fid = 0
    pos = 0

    for i, char in enumerate(data):
        block_size = int(char)

        if i % 2 == 0: # file block
            if block_size == 0:
                raise ValueError("unexpected block_size=0 for file")
            files[fid] = (pos, block_size)
            fid += 1
        else: # blank block
            if block_size != 0: # only track blanks with size > 0
                blanks.append((pos, block_size))
        
        pos += block_size # update position
    
    return files, blanks, fid


def compact_disk_and_calculate_checksum(disk):
    """
    Compact the disk by filling free spaces with file blocks from the end of the disk, then calculate the filesystem checksum.

    Returns the computed filesystem checksum.
    """
    # Find indices of free space blocks (blanks)
    blanks = [i for i, x in enumerate(disk) if x == -1]
    
    for i in blanks:
        
        # remove trailing free space blocks (drop all blanks at the end of the disk)
        while disk[-1] == -1:
            disk.pop()

        # if we've reached the end of the disk, break
        if len(disk) <= i:
            break

        # move the last block to the current free space (assign last element of disk to current index)
        disk[i] = disk.pop()
    
    # calculate checksum by multiplying block index with file ID and summing all products
    return (sum(i * x for i, x in enumerate(disk)))


def compact_files_by_whole_blocks_and_calculate_checksum(files, blanks, fid):
    """
    Compact the disk by moving whole files into free spaces, in decreasing file ID order.

    Returns the computed filesystem checksum after compacting the disk.
    """
    # go through each file and moving it to the first available blank
    while fid > 0:
        fid -= 1
        pos, size = files[fid]
        # go through each available blank
        for i, (start, length) in enumerate(blanks):
            if start >= pos: # blank is after file
                blanks = blanks[:i] # gets rid of extraneous blanks we don't need
                break
            if size <= length: # file fits in blank
                # move file to blank
                files[fid] = (start, size)
                if size == length: # blank no longer exists
                    blanks.pop(i) # delete blank
                else: # blank still has space left
                    blanks[i] = (start + size, length - size)
                break
    
    # calculate checksum
    checksum = 0

    for fid, (pos, size) in files.items():
        for x in range(pos, pos + size):
            checksum += fid * x

    return checksum


if __name__ == "__main__":
    # part 1
    print(compact_disk_and_calculate_checksum(read_input_p1('input.txt')))

    # part 2
    print(compact_files_by_whole_blocks_and_calculate_checksum(*read_input_p2('input.txt')))
