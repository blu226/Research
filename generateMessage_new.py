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

    path = line_arr[4:]

    generateMessage = True

    if len(set(path)) >2:
        for nodeId in path:
            if int(nodeId) > NoOfSources + NoOfDataCenters:
                generateMessage = True

    t = random.randint(int(0.5 * 30), int(1.5 * 30))

    rand = random.uniform(0, 1)

    if generateMessage == True and rand < 0.3 and src < NoOfSources and des >= NoOfSources and des < NoOfSources + NoOfDataCenters:

        p = random.uniform(0, 1)

        if p < 0.25:
            message_file.write(
                str(id) + "\t" + str(src) + "\t" + str(des) + "\t" + str(desired_TTL) + "\t" + str(size) + "\t" + str(
                    t) + "\n")
        else:
            message_file.write(
                str(id) + "\t" + str(src) + "\t" + str(des) + "\t" + str(desired_TTL) + "\t" + str(size) + "\t" + str(
                    genT) + "\n")

        # print(str(id) + "\t" + str(src) + "\t" + str(des) + "\t" + str(desired_TTL) + "\t" + str(size) + "\t" + str(genT) )

        id += 1


