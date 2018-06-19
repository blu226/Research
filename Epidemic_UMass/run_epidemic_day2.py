import os
from STB_help import *

#Take some inputs
#number_of_runs = input("Input number of runs?  ")
#generate_files = input("Do you want to generate the trajectory files?Y/N  ")
def create_new_constants_file(day, V, T, directory, time):
    os.system('rm constants.py')
    f = open("constants.py", "w")
    f.write("numSpec = 4\ndt = 1\ntau = 1\n")
    f.write("minBW = [3,8,20,40]\nmaxBW = [6,20,30,60]\nspectRange = [1800,460,1200,350]\nspectPower = [1,1,1,1]\nepsilon = 0.5\n")
    f.write("t_sd = 0.5\nt_td = 1\nidle_channel_prob = 0.5\nswitching_delay = 0.001\nsensing_power = 0.04\nlambda_val = 1\nmessageBurst = [2, 5]\n\n")
    f.write("debug_message = -1\n")
    f.write("NoOfSources = 6\nNoOfDataCenters = 3\n")
    f.write("TTL = 30\nminTTL=15\nmaxTau = 30\nM = [1,10,25,50,100,500,750,1000]\n")
    f.write("consumedEnergyFile = \'energy_metrics.txt\'\n")
    NoOfDMs = V - 9
    link_exists = "Link_Exists_path = '../Bands_UMass" + str(V) + "/" + directory + "Day2/" + "\'\n"
    delivery_file_name = "delivery_file_name = \"delivery_day" + str(day)+ "_Epi.txt\"\n"
    notDel = "notDelivered_file_name = \'not_delivered_messages_Epi.txt\'\n"
    file_day = "day = " + "\'" + directory + '\'\n'
    metrics_file_name = "metrics_file_name = \"metrics_LLC_day" +str(day) + "_Epi.txt\"\n"
    lex_data_file_name = "lex_data_directory = \"../DataMules/" + directory + "\"\n"

    dir2 = "validate_data_directory = \"../DataMules/" + directory + "Day2/\"\n"
    dir3 = "lex_data_directory_day = \"../DataMules/" + directory + "Day2/\"\n"
    DM_line = "NoOfDMs = " + str(NoOfDMs) + "\n"
    T_line = "T = " + str(T) + "\n"
    V_line = "V = " + str(V) + "\n"
    time_line = "startTime = " + str(time) + '\n'
    num_mess = "num_messages = 300\n"
    message_line = "generated_messages_file = \'../Bands_UMass20/2007-11-06_2007-11-07/Day1/generated_messages.txt\'\n"
    DataMule_path = "DataMule_path = \'../DataMules/\' +  day + \'Day2/\'" + "\n"
    pkl_line = "pkl_folder = lex_data_directory + \"Day" + str(day) + "_pkl/\"\n"
    f.write(file_day)
    f.write(DM_line)
    f.write(DataMule_path)
    f.write(T_line)
    f.write(V_line)
    f.write(num_mess)
    f.write(time_line)
    f.write(link_exists)
    f.write(lex_data_file_name)
    f.write(str(delivery_file_name))
    f.write(notDel)
    f.write(str(metrics_file_name))
    f.write(dir2)
    # f.write(dir3)

    f.write(message_line)
    f.write(pkl_line)
    f.close()
#    os.system('cat constants.py')

def run_simulation_files(day, V, T,directory,time):
    print("_________________________________________________")
    print("Day: ", str(day), " V: ", str(V), " T: ", str(T))

    create_new_constants_file(day, V, T,directory,time)
    #getSrcDst(time, directory)



    run = [0]
    link_exists_folder = "../Bands_UMass" + str(V) + "/" + directory + "Day2/"


    for ind in run:
        # for run in range(1, 4):
        if ind == 0:
            S = [0, 1, 2, 3]
            path_to_folder = link_exists_folder + "ALL/"
            print("\nALL -----------------------")

        elif ind == 1:
            S = [0]
            path_to_folder = link_exists_folder + "TV/"
            print("\nTV ----------------------  ")

        elif ind == 3:
            S = [1]
            path_to_folder = link_exists_folder + "ISM/"
            print("\nISM ------------------------ ")

        elif ind == 2:
            S = [2]
            path_to_folder = link_exists_folder + "LTE/"
            print("\nLTE ----------------------------")

        elif ind == 4:
            S = [3]
            path_to_folder = link_exists_folder + "CBRS/"
            print("\nCBRS --------------------------- ")

        path_to_folder = path_to_folder + "Epidemic/"

        if not os.path.exists(path_to_folder):
            os.makedirs(path_to_folder)

        with open("constants.py", "r") as f:
            lines = f.readlines()

        with open("constants.py", "w") as f:
            for line in lines:
                if ("path_to_folder" not in line) and ("S = " not in line):
                    f.write(line)

            f.write("path_to_folder = '" + str(path_to_folder) + "'\n")
            f.write("S = " + str(S) + "\n")


        # os.system('python3 main.py')
        os.system('python3 metrics.py')


#main
dir = "../DataMules/"

directorys = ['2007-11-06_2007-11-07/']
for i in range(len(directorys)):
    # path = dir + directorys[i] + "Day2"
    # files = findfiles(path)
    # v = len(files)

    for v in range(20, 11, -2):
        run_simulation_files(2, v, 120, directorys[i], 0)












