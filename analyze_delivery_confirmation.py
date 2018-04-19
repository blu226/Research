from constants import *
import csv
from operator import itemgetter


reader = csv.reader(open(path_to_folder + "delivery_day1.txt"), delimiter="\t")

output = open(path_to_folder  + "sorted_delivery_day1.txt", 'w')
for line in sorted(reader, key=itemgetter(0)):
    for n in line:
        output.write(n + " ")
    output.write("\n")

output.close()


reader = csv.reader(open(path_to_folder + "LLC_PATH.txt"), delimiter="\t")

output = open(path_to_folder  + "sorted_LLC_path.txt", 'w')
for line in sorted(reader, key=itemgetter(0)):
    for n in line:
        output.write(n + " ")
    output.write("\n")

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
