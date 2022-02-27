import mem
import sys

clock_pattern = r'\d{2}:\d{2}:\d{2}.\d{3}'
sys_mem_pattern = r'System memory:'
uptime = r'Uptime.\d'

# since we are using "System memory:" as the regex, we need 4 lines down to meet the beginning of the table and get the first process listed
sys_mem_pattern_offset = 4

lines_of_dates, lines_where_sys_mem_starts = [], []
number_of_process = 16

if len(sys.argv) == 2:
    lines_of_dates = mem.searchForLines(
        file=sys.argv[1], pattern=clock_pattern)
    lines_where_sys_mem_starts = mem.searchForLines(
        file=sys.argv[1], pattern=sys_mem_pattern)

    for i in range(1, len(lines_of_dates)):

        mem.compare_process(
            lines_where_sys_mem_starts[-i-1], lines_where_sys_mem_starts[-i], number_of_process, sys_mem_pattern_offset, sys.argv[-i], sys.argv[-i])

else:
    for i in range(1, len(sys.argv)-1):
        lines_where_sys_mem_starts_sample1 = mem.searchForLines(
            file=sys.argv[-i-1], pattern=sys_mem_pattern)

        lines_where_sys_mem_starts_sample2 = mem.searchForLines(
            file=sys.argv[-i], pattern=sys_mem_pattern)

        mem.compare_process(
            lines_where_sys_mem_starts_sample1, lines_where_sys_mem_starts_sample2, number_of_process, sys_mem_pattern_offset, sys.argv[-i-1], sys.argv[-i])
