import os

#Take some inputs
#number_of_runs = input("Input number of runs?  ")
#generate_files = input("Do you want to generate the trajectory files?Y/N  ")

def run_simulation_files(mules, T, max_nodes, run):
    #4, 1, 2
    band_types = [0]
    for ind in band_types:
        # for run in range(1, 4):
        if ind == 0:
            S = [0, 1, 2, 3]
            path_to_folder = "../Bands" + str(mules) + "/" + str(run) + "/Day1/ALL/"
            print("\nALL -----------------------")

        elif ind == 1:
            S = [0]
            path_to_folder = "../Bands" + str(mules) + "/" + str(run) + "/Day1/TV/"
            print("\nTV ----------------------  ")

        elif ind == 3:
            S = [1]
            path_to_folder = "../Bands" + str(mules) + "/" + str(run) + "/Day1/ISM/"
            print("\nISM ------------------------ ")

        elif ind == 2:
            S = [2]
            path_to_folder = "../Bands" + str(mules) + "/" + str(run) + "/Day1/LTE/"
            print("\nLTE ----------------------------")

        elif ind == 4:
            S = [3]
            path_to_folder = "../Bands" + str(mules) + "/" + str(run) + "/Day1/CBRS/"
            print("\nCBRS --------------------------- ")

        # Set correct folder names
        link_exists_folder = "../Bands" + str(mules) + "/" + str(run) + "/Day1/"
        lex_data_directory = "../Lexington" + str(mules) + "/" + str(run) + "/"
        lex_data_directory_day = "../Lexington" + str(mules) + "/" + str(run) + "/Day1/"
        validate_data_directory = "../Lexington" + str(mules) + "/" + str(run) + "/Day1/"

        with open("constants.py", "r") as f:
            lines = f.readlines()

        with open("constants.py", "w") as f:
            for line in lines:
                if ("path_to_folder" not in line) and ("S = " not in line) and (
                    "validate_data_directory" not in line) \
                        and ("link_exists_folder" not in line) and ("lex_data_directory" not in line):
                    f.write(line)


            f.write("path_to_folder = '" + str(path_to_folder) + "'\n")
            f.write("S = " + str(S) + "\n")
            f.write("validate_data_directory = '" + str(validate_data_directory) + "'\n")
            f.write("lex_data_directory = '" + str(lex_data_directory) + "'\n")
            f.write("lex_data_directory_day = '" + str(lex_data_directory_day) + "'\n")
            f.write("link_exists_folder = '" + str(link_exists_folder) + "'\n")

        # print("Folder: Band" + str(mules) + " Band Type: " + str(ind) + " Round: " + str(run))

        os.system('python3 STB_main_path.py')
        
        if ind == 0 and mules == max_nodes:
        	os.system('python3 generateMessage_new.py')

        os.system('python3 main2.py')
        os.system('python3 metrics.py')


number_of_runs = 1
generate_files = "Y"
# generate_files = "N"
#TODO: Generate the trajectory files
if generate_files == "Y":
    print("Generate bus trajectories ---------------------- \n")

    set_max_nodes = True
    max_nodes = 15
    src_des_nodes = 12
    run_start_time = 1

    mule_set = [15]

    for max_mules in mule_set:
        for run in range(run_start_time, 2):
            print("=============== Folder: Band" + str(max_mules) + " Round: " + str(run))

            S = [0, 1, 2, 3]
            path_to_folder = "../Bands" + str(max_mules) + "/" + str(run) + "/Day1/ALL/"
            link_exists_folder = "../Bands" + str(max_mules) + "/" + str(run) +"/Day1/"
            lex_data_directory = "../Lexington" + str(max_mules) + "/" + str(run) +"/"
            lex_data_directory_day = "../Lexington" + str(max_mules) + "/" + str(run) + "/Day1/"
            pkl_folder = "../Lexington" + str(max_mules) + "/" + str(run) + "/Day1_pkl/"
            validate_pkl_folder = "../Lexington" + str(max_mules) + "/" + str(run) + "/Day1_pkl/"
            T = 30

            if set_max_nodes == True:
                # max_nodes = max_mules
                set_max_nodes = False

            with open("constants.py", "r") as f:
                lines = f.readlines()

            with open("constants.py", "w") as f:
                for line in lines:
                    if ("path_to_folder" not in line) and ("S = " not in line) \
                            and ("link_exists_folder" not in line) \
                            and ("lex_data_directory" not in line) \
                            and ("V = " not in line) and ("NoOfDMs = " not in line) and ("T = " not in line) \
                            and ("max_nodes = " not in line) \
                            and ("delivery_file_name" not in line) \
                            and ("metrics_file_name" not in line) \
                            and ("VMIN" not in line) and ("VMAX" not in line)\
                            and ("wait_time" not in line) and ("run_start_time" not in line) \
                            and ("pkl_folder" not in line) and ("validate_pkl_folder" not in line):
                        f.write(line)
                
                f.write("max_nodes = " + str(max_nodes) + "\n")
                f.write("T = " + str(T) + "\n")
                f.write("V = " + str(max_mules + src_des_nodes) + "\n")
                f.write("NoOfDMs = " + str(max_mules) + "\n")
                f.write("path_to_folder = '" + str(path_to_folder) + "'\n")
                f.write("S = " + str(S) + "\n")
                f.write("lex_data_directory = '" + str(lex_data_directory) + "'\n")
                f.write("lex_data_directory_day = '" + str(lex_data_directory_day) + "'\n")
                f.write("link_exists_folder = '" + str(link_exists_folder) + "'\n")
                f.write("delivery_file_name = " + '"delivery_day1.txt"' + "\n")
                f.write("metrics_file_name = " + '"metrics_LLC_day1.txt"' + "\n")
                f.write("VMIN = 100" + "\n")
                f.write("VMAX = 150" + "\n")
                f.write("wait_time = [2, 5]" + "\n")
                f.write("run_start_time = "  + str(run_start_time) + "\n")
                f.write("pkl_folder = '" + pkl_folder + "'\n")
                f.write("validate_pkl_folder = '" + validate_pkl_folder + "'\n")

            os.system('python3 readLexingtonData_Fixed.py')
            os.system('python3 create_pickles_Lex.py')
            os.system('python3 computeLINKEXISTS_Lex.py')
            run_simulation_files(max_mules, T, max_nodes, run)

else:
    print("\n================ Trajectory files were NOT regenerated. \n")
