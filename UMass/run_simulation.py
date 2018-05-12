import os

#Take some inputs
#number_of_runs = input("Input number of runs?  ")
#generate_files = input("Do you want to generate the trajectory files?Y/N  ")
def create_new_constants_file(day, V, T):
    os.system('rm constants.py')
    f = open("constants.py", "w")
    f.write("minX = 0\nmaxX = 100\nminY = 0\nmaxY = 100\nroute_start_time1 = 0\nroute_start_time2 = 15\ndt = 1\ntau = 1\n")
    f.write("minBW = [3,8,20,40\nmaxBW = [6,20,30,60]\nspectRange = [2700,690,1800,540]\nspectPower = [1,1,1,1]\nepsilon = 0.5\n")
    f.write("t_sd = 0.5\nt_td = 1\nidle_channel_prob = 0.5\nswitching_delay = 0.001\nsensing_power = 0.04\nlambda_val = 1\nmessageBurst = [2, 5]\n\n")
    f.write("link_exists_folder = 'Bands/'\nlex_data_directory = 'DataMules/2007-11-03_2007-11-04/'\n")
    f.write("NoOfSources = 6\nNoOfDataCenters = 3\n")
    
    NoOfDMs = V - 9
    delivery_file_name = "delivery_day" + str(day) +"_" + str(V) + "_" + str(T) + ".txt"
    metrics_file_name = "metrics_LLC_day" +str(day)+"_" + str(V) + "_" + str(T)  + ".txt"
    
    f.write("NoOfDMs = " + str(NoOfDMs))
    f.write("T = " + str(T) + "\n")
    f.write("V = " + str(V) + "\n")
    f.write("delivery_file_name = " + str(delivery_file_name))
    f.write("metrics_file_name = " + str(metrics_file_name))
    f.write("lex_data_directory_day = 'DataMules/2007-11-03_2007-11-04/Day" + str(day) + "/'\n")
    f.write("validate_data_directory = 'DataMules/2007-11-03_2007-11-04/Day" + str(day) = "/'\n")
    f. write("StartTime = 850\n")
    f.close()
    
def run_simulation_files(day, V, T):

    create_new_constants_file(day, V, T)

    if day == 1:
        run = [0,1,2,3]
    else:
        run = [0]

    for ind in run:
        # for run in range(1, 4):
        if ind == 0:
            S = [0, 1, 2, 3]
            path_to_folder = "Bands" + "/ALL/"
            print("\nALL -----------------------")

        elif ind == 1:
            S = [0]
            path_to_folder = "Bands" + "/TV/"
            print("\nTV ----------------------  ")

        elif ind == 3:
            S = [1]
            path_to_folder = "Bands" + "/ISM/"
            print("\nISM ------------------------ ")

        elif ind == 2:
            S = [2]
            path_to_folder = "Bands" + "/LTE/"
            print("\nLTE ----------------------------")

        elif ind == 4:
            S = [3]
            path_to_folder = "Bands" + "/CBRS/"
            print("\nCBRS --------------------------- ")

        with open("constants.py", "r") as f:
            lines = f.readlines()

        with open("constants.py", "w") as f:
            for line in lines:
                if ("path_to_folder" not in line) and ("S = " not in line):
                    f.write(line)

            f.write("path_to_folder = '" + str(path_to_folder) + "'\n")
            f.write("S = " + str(S) + "\n")


        #print("Folder: Band" + str(mules) + " Band Type: " + str(ind) + " Round: " + str(run))
##        if ind == 0:
##            os.system('python3 computeLINKEXISTS_UMass.py')

        os.system('python3 STB_main_path.py')
        if ind == 0:
            os.system('python3 generateMessage_new.py')
        os.system('python3 main2.py')
        os.system('python3 metrics.py')


#main
# os.system('python3 createSrcDst.py')
#run_simulation_files(day, V, T)

run_simulation_files(1,16,15)
run_simulation_files(1,16,30)
run_simulation_files(1,16,60)
run_simulation_files(1,16,120)

run_simulation_files(2,16,15)
run_simulation_files(2,16,30)
run_simulation_files(2,16,60)
run_simulation_files(2,16,120)

run_simulation_files(1,11,120)
run_simulation_files(1,12,120)
run_simulation_files(1,13,120)
run_simulation_files(1,14,120)
run_simulation_files(1,15,120)

run_simulation_files(2,11,120)
run_simulation_files(2,12,120)
run_simulation_files(2,13,120)
run_simulation_files(2,14,120)
run_simulation_files(2,15,120)









