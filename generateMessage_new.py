from constants import *
import random

message_file = open(link_exists_folder + "generated_messages.txt", "w")
with open(path_to_folder + "LLC_PATH.txt", "r") as fp:
    path_lines = fp.readlines()[1:]
fp.close()

id = 0

for line in path_lines:
    line_arr = line.strip().split()

    src = int(line_arr[0])
    des = int(line_arr[1])
    genT = int(line_arr[2])
    size = int(line_arr[3])
    desired_TTL = random.randint(minTTL, TTL)

    t = random.randint(0, int(1.5 * T))

    if src < NoOfSources + NoOfDataCenters and des < NoOfSources + NoOfDataCenters:
        message_file.write(
            str(id) + "\t" + str(src) + "\t" + str(des) + "\t" + str(desired_TTL) + "\t" + str(size) + "\t" + str(
                t) + "\n")
        # print(str(id) + "\t" + str(src) + "\t" + str(des) + "\t" + str(desired_TTL) + "\t" + str(size) + "\t" + str(genT) )

        id += 1


