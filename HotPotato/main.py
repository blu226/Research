#MAIN
from network import *
import pickle
import os

#Function create_constants: creates a constants file for the given simulation
def create_constants(dir, startTime):
    day_directory = "day = " + "\'" + dir + "\'\n"
    Link_Exists_path = "Link_Exists_path = \'../Bands_UMass/\' + day" +  "\n"
    DataMule_path = "DataMule_path = \'../DataMules/\' +  day + \'Day1/\'" + "\n"
    time = "startTime = " + str(startTime) + "\n"
    metrics = "metrics_file_name = \'metrics_MF.txt\'\n"
    delivery = "delivery_file_name = \'delivered_messages_MF.txt\'\n"
    genM = "generated_messages_file = \'../Bands_UMass/\' + day + \'generated_messages.txt\'\n"
    specRan = "spectRange = [3600,920,2400,700]\n"
    notDel = "notDelivered_file_name = \'not_delivered_messages_MF.txt\'\n"
    debug_mes = "debug_message = -1\n"
    power_var = "t_sd = 0.5\nt_td = 1\nidle_channel_prob = 0.5\ntau = 1\n"


    f = open("constants.py", "w")

    f.write(day_directory)
    f.write(Link_Exists_path)
    f.write(DataMule_path)
    f.write(metrics)
    f.write(delivery)
    f.write(notDel)
    f.write(genM)
    f.write(specRan)
    f.write(time)
    f.write(debug_mes)
    f.write(power_var)
    f.write("M = [1,10,25,50,100,500,750,1000]\n")
    f.write("maxTau = 10\n")
    f.write("num_messages = 100\n")
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

# time = 0
    # print(day)

def MF_simulation():
    # Create constants
    #create_constants(dir,time)

    if not os.path.exists(path_to_folder):
        os.makedirs(path_to_folder)

    output_file = open(path_to_folder + delivery_file_name, "w")
    output_file.write("ID\ts\td\tts\tte\tLLC\tsize\tparent\n")
    output_file.write("----------------------------------------------------\n")
    output_file.close()

    output_file2 = open(path_to_folder + notDelivered_file_name, "w")
    output_file2.write("ID\ts\td\tts\tte\tLLC\tsize\tparent\n")
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



    #Create network
    net = network()
    #Fill network with datamules, sources, and destinations
    net.fill_network()
    #Create messages
    # path = "Bands/" + day + "/"
    # create_messages(path)

    message_path_file = "../Bands" + str(max_nodes) + "/" + Link_Exists_path.split("/")[
        2] + "/Day1/" + "generated_messages.txt"
    print(message_path_file)
    with open(message_path_file, "r") as f:
        msg_lines = f.readlines()[1:]

    #Run simulation
    for i in range(T):
        # print("TIME: " + str(i))
        net.network_GO(i , LINK_EXISTS, specBW, msg_lines)

    net.all_messages()

MF_simulation()
