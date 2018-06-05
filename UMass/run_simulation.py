import os
from createSrcDst import *

#Take some inputs
#number_of_runs = input("Input number of runs?  ")
#generate_files = input("Do you want to generate the trajectory files?Y/N  ")
def create_new_constants_file(day, V, T, directory, time):
    os.system('rm constants.py')
    f = open("constants.py", "w")
    f.write("numSpec = 4\nminX = 0\nmaxX = 100\nminY = 0\nmaxY = 100\nroute_start_time1 = 0\nroute_start_time2 = 15\ndt = 1\ntau = 1\n")
    f.write("minBW = [3,8,20,40]\nmaxBW = [6,20,30,60]\nspectRange = [3600,920,2400,700]\nspectPower = [1,1,1,1]\nepsilon = 0.5\n")
    f.write("t_sd = 0.5\nt_td = 1\nidle_channel_prob = 0.5\nswitching_delay = 0.001\nsensing_power = 0.04\nlambda_val = 1\nmessageBurst = [2, 5]\n\n")
    f.write("NoOfSources = 6\nNoOfDataCenters = 3\n")
    f.write("TTL = 30\nminTTL=15\nmaxTau = 10\nM = [1,10,25,50,100,500,750,1000]\n")
    NoOfDMs = V - 9
    link_exists = "link_exists_folder = 'Bands/" + directory +"\'\n"
    delivery_file_name = "delivery_file_name = \"delivery_day" + str(day) +"_" + str(V) + "_" + str(T) + ".txt\"\n"
    metrics_file_name = "metrics_file_name = \"metrics_LLC_day" +str(day)+"_" + str(V) + "_" + str(T)  + ".txt\"\n"
    lex_data_file_name = "lex_data_directory = \"DataMules/" + directory + "\"\n"
    if day == 1:
        dir2 = "validate_data_directory = \"DataMules/" + directory + "Day1/\"\n"
        dir3 = "lex_data_directory_day = \"DataMules/" + directory + "Day1/\"\n"
    else:
        dir2 = "validate_data_directory = \"DataMules/" + directory + "Day2/\"\n"
        dir3 = "lex_data_directory_day = \"DataMules/" + directory + "Day2/\"\n"
    DM_line = "NoOfDMs = " + str(NoOfDMs) + "\n"
    T_line = "T = " + str(T) + "\n"
    V_line = "V = " + str(V) + "\n"
    time_line = "StartTime = " + str(time) + '\n'
    f.write(link_exists)
    f.write(lex_data_file_name)
    f.write(DM_line)
    f.write(T_line)
    f.write(V_line)
    f.write(str(delivery_file_name))
    f.write(str(metrics_file_name))
    f.write(dir2)
    f.write(dir3)
    f. write(time_line)
    f.close()
#    os.system('cat constants.py')
    
def run_simulation_files(day, V, T,directory,time):
    print("_________________________________________________") 
    print("Day: ", str(day), " V: ", str(V), " T: ", str(T))

    create_new_constants_file(day, V, T,directory,time)
    getSrcDst(time, directory)

    if day == 1:
        run = [0]
    else:
        run = [0]

    for ind in run:
        # for run in range(1, 4):
        if ind == 0:
            S = [0, 1, 2, 3]
            path_to_folder = "Bands/" + directory+ "ALL/"
            print("\nALL -----------------------")

        elif ind == 1:
            S = [0]
            path_to_folder = "Bands/" + directory + "TV/"
            print("\nTV ----------------------  ")

        elif ind == 3:
            S = [1]
            path_to_folder = "Bands/" + directory +"ISM/"
            print("\nISM ------------------------ ")

        elif ind == 2:
            S = [2]
            path_to_folder = "Bands/" + directory + "LTE/"
            print("\nLTE ----------------------------")

        elif ind == 4:
            S = [3]
            path_to_folder = "Bands/" + directory + "CBRS/"
            print("\nCBRS --------------------------- ")

        with open("constants.py", "r") as f:
            lines = f.readlines()

        with open("constants.py", "w") as f:
            for line in lines:
                if ("path_to_folder" not in line) and ("S = " not in line):
                    f.write(line)

            f.write("path_to_folder = '" + str(path_to_folder) + "'\n")
            f.write("S = " + str(S) + "\n")


        # #print("Folder: Band" + str(mules) + " Band Type: " + str(ind) + " Round: " + str(run))
        # if ind == 0 and day == 1:
        #    os.system('python3 computeLINKEXISTS_UMass.py')

        os.system('python3 STB_main_path.py')
        if ind == 0 and day == 1:
            os.system('python3 generateMessage_new.py')
        os.system('python3 main2.py')
        os.system('python3 metrics.py')


#main
# os.system('python3 createSrcDst.py')
#run_simulation_files(day, V, T)
dir = "DataMules/"
# directorys = ['2007-10-23_2007-10-24/', '2007-10-24_2007-10-25/', '2007-10-25_2007-10-26/', '2007-10-26_2007-10-27/','2007-10-29_2007-10-30/','2007-10-30_2007-10-31/','2007-10-31_2007-11-01/','2007-11-01_2007-11-02/','2007-11-02_2007-11-03/','2007-11-03_2007-11-04/','2007-11-04_2007-11-05/','2007-11-05_2007-11-06/','2007-11-06_2007-11-07/','2007-11-07_2007-11-08/','2007-11-09_2007-11-10/','2007-11-10_2007-11-11/']
# startTime = [800,800,680,920,680,920,680,920,680,560,800,560,680,560,800,560,800,560]
# directorys = ['2007-11-03_2007-11-05/']
# startTime = [800]
directorys = ['2007-10-25_2007-10-26/']
startTime = [800]
for i in range(len(directorys)):
    path = dir + directorys[i] + "Day1"
    files = findfiles(path)
    v = len(files)

    run_simulation_files(1,v,120, directorys[i], startTime[i])
    run_simulation_files(2,v,120, directorys[i], startTime[i])











