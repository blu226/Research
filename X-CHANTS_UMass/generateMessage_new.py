from constants import *
import random

message_file = open(generated_messages_file, "w")
path_to_LLC_arr = path_to_folder.split('/')
path_to_Day1_LLC = path_to_LLC_arr[0] + "/" + path_to_LLC_arr[1] + '/' + path_to_LLC_arr[2] + '/Day1/' + path_to_LLC_arr[4] + '/' + path_to_LLC_arr[5] + '/' + path_to_LLC_arr[6] + '/'

with open(path_to_Day1_LLC + "LLC_PATH.txt", "r") as fp:
    path_lines = fp.readlines()[1:]
fp.close()

id = 0
message_file.write("ID\ts\td\tTTL\tsize\tgenT\n")
while id < 100:
    # print(id)
    rand_line = random.choice(path_lines)
    path_lines.remove(rand_line)
    line_arr = rand_line.strip().split()

    src = int(line_arr[0])
    des = int(line_arr[1])
    genT = int(line_arr[2])
    size = int(line_arr[3])
    desired_TTL = random.randint(minTTL, TTL)

    path = line_arr[4:]

    generateMessage = False

    if len(set(path)) >2:
        for nodeId in path:
            if int(nodeId) >= NoOfSources + NoOfDataCenters:
                generateMessage = True

    t = random.randint(int(.1 * T), int(.25 * T))

    #rand = random.uniform(0, 1)

    if generateMessage == True  and src < NoOfSources and  des >= NoOfSources and des < NoOfSources + NoOfDataCenters and genT <= .25 * T:

        p = random.uniform(0, 1)

        if p < 0.05:
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


