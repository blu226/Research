from constants import *
import random

message_file = open(generated_message_file, "w")
with open(path_to_folder + "LLC_PATH.txt", "r") as fp:
    path_lines = fp.readlines()[1:]
fp.close()

id = 0
message_file.write("ID\ts\td\tTTL\tsize\tgenT\n")
while id < 10:
    rand_line = random.randint(0, len(path_lines) - 1)
    line_arr = path_lines[rand_line].strip().split()

    src = int(line_arr[0])
    des = int(line_arr[1])
    genT = int(line_arr[2])
    size = int(line_arr[3])
    desired_TTL = random.randint(minTTL, TTL)

    path = line_arr[4:]

    generateMessage = True

    # if len(set(path)) >2:
    #     for nodeId in path:
    #         if int(nodeId) <= NoOfDMs:
    #             generateMessage = True

    t = random.randint(int(45), int(60))

    #rand = random.uniform(0, 1)

    if generateMessage == True  and src < NoOfSources and  des >= NoOfSources and des <= NoOfSources + NoOfDataCenters and genT <= 60:

        p = random.uniform(0, 1)

        if p < 0:
            message_file.write(
                str(id) + "\t" + str(src) + "\t" + str(des) + "\t" + str(desired_TTL) + "\t" + str(size) + "\t" + str(
                    t) + "\n")
        else:
            message_file.write(
                str(id) + "\t" + str(src) + "\t" + str(des) + "\t" + str(desired_TTL) + "\t" + str(size) + "\t" + str(
                    genT) + "\n")

        # print(str(id) + "\t" + str(src) + "\t" + str(des) + "\t" + str(desired_TTL) + "\t" + str(size) + "\t" + str(genT) )

        id += 1
        # if id > 500:
        #     break


