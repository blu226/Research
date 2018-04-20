import random
import math
from constants import *


# def get_message_path(t, src, des):
#     with open(path_to_folder + "LLC_PATH")
#     return ("1")

# Generate a list of messages at each time [0, T] at every source node

def generate_messages():
    message_file = open("generated_messages.txt", "w")
    genT = 0
    id = 0
    message_file.write("#id\tsrc\tdes\tTTL\tSize\tgenT\n")
    while genT < T:
        # t += 1
        for src in range(NoOfSources):
            message_burst = random.randint(int(messageBurst[0]), messageBurst[1])
            #Number of messages generated at this source at this time
            for num in range(message_burst):
                des = random.randint(NoOfSources + NoOfDMs, V - 1)
                TTL = random.randint(genT, T)
                size = 20

                print(str(id) + "\t" + str(src) + "\t" + str(des) + "\t" + str(TTL) + "\t" +  str(size) + "\t" + str(genT))
                message_file.write(str(id) + "\t" + str(src) + "\t" + str(des) + "\t" + str(TTL) + "\t" +  str(size) + "\t" + str(genT) + "\n")
                id += 1

        num =  1 * lambda_val * genT
        genT = int(lambda_val * math.exp(num))

    message_file.close()

#Main starts here

generate_messages()




