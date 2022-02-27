import re
import sys


# Based on a given file and pattern, search for the lines in the file that match with the pattern and return a list containing the lines.
def searchForLines(file, pattern):

    start_line = 0
    lines_list = []

    p = re.compile(pattern)

    with open(file) as f:

        for line in f:

            if p.findall(line):

                lines_list.append(start_line)

            start_line += 1

    # In case we are comparing between files
    if len(lines_list) == 1:
        return lines_list.pop()

    # When the same file has more than 1 ocurrance of the pattern we are searching for
    return lines_list


# Parse a line and offset (to get next line/process) to return the name of the process and the RSS value.
def getProcess(starting_point, offset, regex_offset, file):

    with open(file) as f:

        lines = f.readlines()

        process_sample_line_raw = lines[starting_point +
                                        regex_offset + offset]
        process_sample_line_split = " ".join(process_sample_line_raw.split())
        current_line_sample = re.split('\s', process_sample_line_split.strip())

        try:

            current_process_sample = current_line_sample.pop()
            current_process_rss_sample = current_line_sample.pop()

            try:

                return current_process_sample, int(current_process_rss_sample)

            except:

                print('Check output')
                sys.exit(2)

        except:

            print('Change number of process; not enough in the current samples')


# Adding the increment from an offset to add in a file.
def addToFile(file, offset, increment):

    with open(file, "r+") as f:

        lines = f.readlines()

        lines[offset] = lines[offset].rstrip() + f' + {increment:,}\n'
        f.seek(0)

        for line in lines:
            f.write(line)


# Givin the line of the first and second sample, go through by the number of process times. Also give an offset of the regex pattern and file to manipulate
def compare_process(first_sample, second_sample, number_of_processes, regex_offset, file_1, file_2):

    for i in range(number_of_processes):

        # Get second sample process name and RSS value
        get_second_sample = getProcess(second_sample, i, regex_offset, file_2)

        for j in range(number_of_processes):

            # Get first sample process name and RSS value
            get_first_sample = getProcess(
                first_sample, j, regex_offset, file_1)

            # Check if we are comparing the same process name
            if get_second_sample[0] == get_first_sample[0]:

                if get_second_sample[1] > get_first_sample[1]:

                    diff = get_second_sample[1] - get_first_sample[1]

                    addToFile(file_2, second_sample +
                              regex_offset + i, diff)
                    break
