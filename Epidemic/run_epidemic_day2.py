import os

def run_simulation_files(mules, T, max_nodes, run):
    # 4, 1, 2
    band_types = [2, 4, 1, 0, 3]
    for ind in band_types:
        # for run in range(1, 4):
        if ind == 0:
            S = [0, 1, 2, 3]
            path_to_folder = "../Bands" + str(mules) + "/" + str(run) + "/Day2/ALL/"
            print("\nALL -----------------------")

        elif ind == 1:
            S = [0]
            path_to_folder = "../Bands" + str(mules) + "/" + str(run) + "/Day2/TV/"
            print("\nTV ----------------------  ")

        elif ind == 3:
            S = [1]
            path_to_folder = "../Bands" + str(mules) + "/" + str(run) + "/Day2/ISM/"
            print("\nISM ------------------------ ")

        elif ind == 2:
            S = [2]
            path_to_folder = "../Bands" + str(mules) + "/" + str(run) + "/Day2/LTE/"
            print("\nLTE ----------------------------")

        elif ind == 4:
            S = [3]
            path_to_folder = "../Bands" + str(mules) + "/" + str(run) + "/Day2/CBRS/"
            print("\nCBRS --------------------------- ")

        path_to_folder = path_to_folder + "Epidemic/"
        # Set correct folder names
        Link_Exists_path = "../Bands" + str(mules) + "/" + str(run) + "/Day2/"
        DataMule_path = "../Lexington" + str(mules) + "/" + str(run) + "/Day2/"
        validate_data_directory = "../Lexington" + str(mules) + "/" + str(run) + "/Day2/"

        with open("constants.py", "r") as f:
            lines = f.readlines()

        with open("constants.py", "w") as f:
            for line in lines:
                if ("path_to_folder" not in line)\
                    and ("Link_Exists_path" not in line)\
                    and ("S = " not in line)\
                    and ("DataMule_path" not in line):
                    f.write(line)


            f.write("path_to_folder = '" + str(path_to_folder) + "'\n")
            f.write("S = " + str(S) + "\n")
            #f.write("validate_data_directory = '" + str(validate_data_directory) + "'\n")
            f.write("DataMule_path = '" + str(DataMule_path) + "'\n")
            f.write("Link_Exists_path = '" + str(Link_Exists_path) + "'\n")

        os.system('python3 main.py')
        os.system('python3 metrics.py')

set_max_nodes = True
max_nodes = 10

mule_set = [10]
run_start_time = 1

for max_mules in mule_set:
    for run in range(run_start_time, 2):
        print("=============== Folder: Band" + str(max_mules) + " Round: " + str(run))

        S = [0, 1, 2, 3]
        path_to_folder = "../Bands" + str(max_mules) + "/" + str(run) + "/Day2/ALL/Epidemic/"
        Link_Exists_path = "../Bands" + str(max_mules) + "/" + str(run) + "/Day2/"
        DataMule_path = "../Lexington" + str(max_mules) + "/" + str(run) + "/Day2/"

        T = 120

        if set_max_nodes == True:
            # max_nodes = max_mules
            set_max_nodes = False
        #Read a file
        with open("constants.py", "r") as f:
            lines = f.readlines()

        #Write to the file
        with open("constants.py", "w") as f:
            for line in lines:
                if ("path_to_folder" not in line) and ("S = " not in line) \
                        and ("Link_Exists_path" not in line) \
                        and ("DataMule_path" not in line) \
                        and ("T = " not in line) \
                        and ("max_nodes = " not in line) \
                        and ("delivery_file_name" not in line) \
                        and ("metrics_file_name" not in line):
                    f.write(line)

            f.write("path_to_folder = '" + str(path_to_folder) + "'\n")
            f.write("Link_Exists_path = '" + str(Link_Exists_path) + "'\n")
            f.write("DataMule_path = '" + str(DataMule_path) + "'\n")
            f.write("T = " + str(T) + "\n")
            f.write("S = " + str(S) + "\n")
            f.write("V = " + str(max_mules) + "\n")
            f.write("sensing_power = 0.04\n")
            f.write("idle_channel_prob = 0.5\n")
            f.write("switching_delay = 0.001\n")
            f.write("spectPower = [1,1,1,1]\n")
            f.write("max_nodes = " + str(max_nodes) + "\n")
            f.write("delivery_file_name = " + '"delivery_epidemic_day2.txt"' + "\n")
            f.write("metrics_file_name = " + '"metrics_epidemic_day2.txt"' + "\n")
            f.write("consumedEnergyFile = \'energy_metrics.txt\'\n")

        run_simulation_files(max_mules, T, max_nodes, run)