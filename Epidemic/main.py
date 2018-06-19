#MAIN
from network import *
import os
import pickle

def createLinkExistenceADJ():

    LINK_EXISTS = numpy.empty(shape=(5, 5, 4, 7, 7))
    LINK_EXISTS.fill(math.inf)

    for i in range(5):
        for s in range(4):
            for t in range(5, 1):
                LINK_EXISTS[i, i, s, t, t + 1] = 1

    # # t = [0,1]
    # LINK_EXISTS[0, 1, 0, 0, 1] = 1
    # LINK_EXISTS[1, 0, 0, 0, 1] = 1
    # LINK_EXISTS[0, 1, 1, 0, 1] = 1
    # LINK_EXISTS[1, 0, 1, 0, 1] = 1
    # LINK_EXISTS[1, 3, 0, 0, 1] = 1
    # LINK_EXISTS[3, 1, 0, 0, 1] = 1
    #
    # #t = [1,2]
    # LINK_EXISTS[1, 3, 0, 1, 2] = 1
    # LINK_EXISTS[3, 1, 0, 1, 2] = 1
    # LINK_EXISTS[1, 3, 1, 1, 2] = 1
    # LINK_EXISTS[3, 1, 1, 1, 2] = 1
    # LINK_EXISTS[2, 3, 0, 1, 2] = 1
    # LINK_EXISTS[3, 2, 0, 1, 2] = 1
    # LINK_EXISTS[2, 3, 1, 1, 2] = 1
    # LINK_EXISTS[3, 2, 1, 1, 2] = 1
    #
    # # t= [2,3]
    # LINK_EXISTS[0, 1, 0, 2, 3] = 1
    # LINK_EXISTS[1, 0, 0, 2, 3] = 1
    # LINK_EXISTS[1, 3, 0, 2, 3] = 1
    # LINK_EXISTS[3, 1, 0, 2, 3] = 1
    # LINK_EXISTS[2, 3, 0, 2, 3] = 1
    # LINK_EXISTS[3, 2, 0, 2, 3] = 1
    # LINK_EXISTS[2, 3, 1, 2, 3] = 1
    # LINK_EXISTS[3, 2, 1, 2, 3] = 1
    #
    # # t = [3,4]
    # LINK_EXISTS[0, 3, 0, 3, 4] = 1
    # LINK_EXISTS[3, 0, 0, 3, 4] = 1
    # LINK_EXISTS[0, 3, 1, 3, 4] = 1
    # LINK_EXISTS[3, 0, 1, 3, 4] = 1
    # LINK_EXISTS[2, 3, 0, 3, 4] = 1
    # LINK_EXISTS[3, 2, 0, 3, 4] = 1

    # t = [0,1]
    LINK_EXISTS[0, 1, 0, 0, 1] = 1
    LINK_EXISTS[0, 1, 1, 0, 1] = 1
    LINK_EXISTS[0, 2, 0, 0, 1] = 1
    LINK_EXISTS[0, 2, 1, 0, 1] = 1
    LINK_EXISTS[0, 4, 2, 0, 1] = 1
    LINK_EXISTS[1, 2, 0, 0, 1] = 1
    LINK_EXISTS[1, 0, 0, 0, 1] = 1
    LINK_EXISTS[1, 0, 1, 0, 1] = 1
    LINK_EXISTS[2, 0, 0, 0, 1] = 1
    LINK_EXISTS[2, 0, 1, 0, 1] = 1
    LINK_EXISTS[2, 1, 0, 0, 1] = 1
    LINK_EXISTS[2, 3, 1, 0, 1] = 1
    LINK_EXISTS[3, 2, 1, 0, 1] = 1
    LINK_EXISTS[4, 0, 2, 0, 1] = 1

    # t = [1,2]
    LINK_EXISTS[0, 2, 0, 1, 2] = 1
    LINK_EXISTS[0, 3, 2, 1, 2] = 1
    LINK_EXISTS[0, 4, 1, 1, 2] = 1
    LINK_EXISTS[0, 4, 2, 1, 2] = 1
    LINK_EXISTS[1, 2, 1, 1, 2] = 1
    LINK_EXISTS[1, 2, 2, 1, 2] = 1
    LINK_EXISTS[2, 0, 0, 1, 2] = 1
    LINK_EXISTS[2, 1, 1, 1, 2] = 1
    LINK_EXISTS[2, 1, 2, 1, 2] = 1
    LINK_EXISTS[2, 3, 1, 1, 2] = 1
    LINK_EXISTS[3, 0, 2, 1, 2] = 1
    LINK_EXISTS[3, 2, 1, 1, 2] = 1
    LINK_EXISTS[3, 4, 2, 1, 2] = 1
    LINK_EXISTS[4, 0, 0, 1, 2] = 1
    LINK_EXISTS[4, 0, 1, 1, 2] = 1
    LINK_EXISTS[4, 3, 2, 1, 2] = 1

    # t = [2,3]
    LINK_EXISTS[0, 3, 0, 2, 3] = 1
    LINK_EXISTS[0, 3, 1, 2, 3] = 1
    LINK_EXISTS[0, 3, 2, 2, 3] = 1
    LINK_EXISTS[0, 4, 0, 2, 3] = 1
    LINK_EXISTS[0, 4, 1, 2, 3] = 1
    LINK_EXISTS[0, 4, 2, 2, 3] = 1
    LINK_EXISTS[1, 2, 0, 2, 3] = 1
    LINK_EXISTS[2, 1, 0, 2, 3] = 1
    LINK_EXISTS[3, 0, 0, 2, 3] = 1
    LINK_EXISTS[3, 0, 1, 2, 3] = 1
    LINK_EXISTS[3, 0, 2, 2, 3] = 1
    LINK_EXISTS[3, 4, 0, 2, 3] = 1
    LINK_EXISTS[3, 4, 1, 2, 3] = 1
    LINK_EXISTS[3, 4, 2, 2, 3] = 1
    LINK_EXISTS[4, 0, 0, 2, 3] = 1
    LINK_EXISTS[4, 0, 1, 2, 3] = 1
    LINK_EXISTS[4, 0, 2, 2, 3] = 1
    LINK_EXISTS[4, 3, 0, 2, 3] = 1
    LINK_EXISTS[4, 3, 1, 2, 3] = 1
    LINK_EXISTS[4, 3, 2, 2, 3] = 1

    # t = [3,4]
    LINK_EXISTS[0, 1, 0, 3, 4] = 1
    LINK_EXISTS[0, 3, 1, 3, 4] = 1
    LINK_EXISTS[1, 0, 0, 3, 4] = 1
    LINK_EXISTS[1, 3, 0, 3, 4] = 1
    LINK_EXISTS[1, 3, 2, 3, 4] = 1
    LINK_EXISTS[2, 4, 1, 3, 4] = 1
    LINK_EXISTS[3, 0, 1, 3, 4] = 1
    LINK_EXISTS[3, 1, 0, 3, 4] = 1
    LINK_EXISTS[3, 1, 2, 3, 4] = 1
    LINK_EXISTS[4, 2, 1, 3, 4] = 1

    # t = [4,5]
    LINK_EXISTS[0, 1, 0, 4, 5] = 1
    LINK_EXISTS[0, 1, 1, 4, 5] = 1
    LINK_EXISTS[1, 0, 0, 4, 5] = 1
    LINK_EXISTS[1, 0, 1, 4, 5] = 1
    LINK_EXISTS[1, 3, 2, 4, 5] = 1
    LINK_EXISTS[2, 3, 0, 4, 5] = 1
    LINK_EXISTS[3, 1, 2, 4, 5] = 1
    LINK_EXISTS[3, 2, 0, 4, 5] = 1
    LINK_EXISTS[3, 4, 0, 4, 5] = 1
    LINK_EXISTS[4, 3, 0, 4, 5] = 1

    return LINK_EXISTS

#Function create_constants: creates a constants file for the given simulation
def create_constants(startTime):
    Link_Exists_path = "Link_Exists_path = \'Bands_UMass/2007-10-23_2007-10-24/'" + "\n"
    DataMule_path = " DataMule_path = \'DataMules1/2007-10-23_2007-10-24/Day1/\' " + "\n"
    time = "startTime = " + str(startTime) + "\n"

    f = open("constants.py", "w")

    f.write(time)
    f.write(Link_Exists_path)
    f.write(DataMule_path)

    f.write("M = [1,10,25,50,100,500,750,1000]\n")
    f.write("maxTau = 10\n")
    f.write("num_messages = 25\n")
    f.write("num_sources = 6\n")
    f.write("num_des = 3\n")
    f.write("T = 120\n")

    f.close()

#Loop thru each day
# days = os.listdir("Bands/")
# days.sort()

# counter = 0
# for day in days:
#     if counter > 0:
#         break

time = 0

if not os.path.exists(path_to_folder):
    os.makedirs(path_to_folder)

output_file = open(path_to_folder + delivery_file_name, "w")
output_file.write("ID\ts\td\tts\tte\tLLC\tsize\tparent\tparentTime\treplica\n")
output_file.write("----------------------------------------------------\n")
output_file.close()

output_file2 = open(path_to_folder + notDelivered_file_name, "w")
output_file2.write("ID\ts\td\tts\tte\tLLC\tsize\tparent\tparentTime\treplica\n")
output_file2.write("----------------------------------------------------\n")
output_file2.close()

output_file3 = open(path_to_folder + consumedEnergyFile, 'w')
output_file3.write("Time\tEnergy\n")
output_file3.close()
#Load Link Exists
LINK_EXISTS = pickle.load(open(Link_Exists_path + "LINK_EXISTS.pkl", "rb"))
specBW = pickle.load(open(Link_Exists_path + "specBW.pkl", "rb"))
# LINK_EXISTS = createLinkExistenceADJ()
# print(LINK_EXISTS[3,4,])

#Create constants
# create_constants(time)

#Generate Messages
# create_messages()

#Create network
net = network()
#Fill network with datamules, sources, and destinations
net.fill_network()
#Create messages
# path = "Bands/" + day + "/"
# create_messages(path)

message_path_file = "../Bands" + str(max_nodes) + "/" + Link_Exists_path.split("/")[2] + "/Day1/" + "generated_messages.txt"
print(message_path_file)
with open(message_path_file, "r") as f:
    msg_lines = f.readlines()[1:]


#Run simulation
for i in range(T):
    # print("TIME: " + str(i))
    net.network_GO(i , LINK_EXISTS, specBW, msg_lines)

net.all_messages()
