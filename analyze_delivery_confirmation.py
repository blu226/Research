from constants import *
import csv
from operator import itemgetter


reader = csv.reader(open(path_to_folder + "LLC_delivery_confirmation.txt"), delimiter="\t")

output = open(path_to_folder  + "sorted_delivery_confirmation.txt", 'w')
for line in sorted(reader, key=itemgetter(3)):
    output.write(str(line) + "\n")

output.close()

# lines = open(path_to_folder + "LLC_delivery_confirmation.txt", "r").readlines()[2:]
#
# for line in all_lines:
#     line_arr = line.strip().split("\t")
#     print(line_arr[1], line_arr[2])
#
# output = open("sorted_delivery_confirmation.txt", 'w')
#
# for line in sorted(lines, key=itemgetter(0)):
