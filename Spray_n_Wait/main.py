#MAIN
from network import *
import pickle

#Function create_constants: creates a constants file for the given simulation
def create_constants(dir, startTime):
    day_directory = "day = " + "\'" + dir + "\'\n"
    Link_Exists_path = "Link_Exists_path = \'../Bands_UMass/\' + day" +  "\n"
    DataMule_path = "DataMule_path = \'../DataMules/\' +  day + \'Day1/\'" + "\n"
    time = "startTime = " + str(startTime) + "\n"
    metrics = "metrics_file_name = \'metrics_SnW.txt\'\n"
    delivery = "delivery_file_name = \'delivered_messages_SnW.txt\'\n"
    genM = "generated_messages_file = \'../Bands_UMass/\' + day + \'generated_messages.txt\'\n"
    specRan = "spectRange = [3600,920,2400,700]\n"
    notDel = "notDelivered_file_name = \'not_delivered_messages_SnW.txt\'\n"
    num_reps = "num_mess_replicas = 150\n"
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
    f.write(num_reps)
    f.write(debug_mes)
    f.write(power_var)
    f.write("M = [1,10,25,50,100,500,750,1000]\n")
    f.write("maxTau = 10\n")
    f.write("num_messages = 10\n")
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

def spray_n_wait_simulation(dir,time):
    # Create constants
    create_constants(dir,time)


    output_file = open(Link_Exists_path + delivery_file_name, "w")
    output_file.write("ID\ts\td\tts\tte\tLLC\tsize\tparent\treplica\n")
    output_file.write("----------------------------------------------------\n")
    output_file.close()

    output_file2 = open(Link_Exists_path + notDelivered_file_name, "w")
    output_file2.write("ID\ts\td\tts\tte\tLLC\tsize\tparent\treplica\n")
    output_file2.write("----------------------------------------------------\n")
    output_file2.close()
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

    with open(generated_messages_file, "r") as f:
        msg_lines = f.readlines()[1:]

    #Run simulation
    for i in range(T):
        print("TIME: " + str(i))
        net.network_GO(i , LINK_EXISTS, specBW, msg_lines)

    net.all_messages()

spray_n_wait_simulation('2007-10-23_2007-10-24/', 0)
