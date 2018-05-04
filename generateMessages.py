import random
import math
from constants import *

# Generate a list of messages at each time [0, T] at every source node
def generate_messages():
    message_file = open("generated_messages.txt", "w")
    genT = 0
    id = 0
    message_file.write("#id\tsrc\tdes\tTTL\tSize\tgenT\n")

    while genT < 45:
        # t += 1
        number_sources = 0
        while number_sources < 15:
            src = random.randint(0, NoOfSources)
            # for src in range(NoOfSources):
            message_burst = random.randint(int(messageBurst[0]), messageBurst[1])

            #Number of messages generated at this source at this time
            for num in range(message_burst):
                des = random.randint(NoOfSources, NoOfSources + NoOfDataCenters)
                desired_TTL = random.randint(minTTL, TTL)
                rand_size = random.uniform(0, 1)

                # if rand_size <= 0.75:
                size = random.choice(M)
                # else:
                #     size = random.choice(M[3:])

                print(str(id) + "\t" + str(src) + "\t" + str(des) + "\t" + str(desired_TTL) + "\t" +  str(size) + "\t" + str(genT))
                message_file.write(str(id) + "\t" + str(src) + "\t" + str(des) + "\t" + str(desired_TTL) + "\t" +  str(size) + "\t" + str(genT) + "\n")
                id += 1

            number_sources += 1
        genT += random.randint(1, 10)
        # num = 1 * lambda_val * genT
        # genT = int(lambda_val * math.exp(num))

    message_file.close()

#Main starts here

generate_messages()




