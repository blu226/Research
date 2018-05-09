import os

#Take some inputs
#number_of_runs = input("Input number of runs?  ")
#generate_files = input("Do you want to generate the trajectory files?Y/N  ")

def run_simulation_files(mules, T, max_nodes, run):

    band_types = [0, 3, 4, 1, 2]
    for ind in band_types:
        # for run in range(1, 4):
        if ind == 0:
            S = [0, 1, 2, 3]
            path_to_folder = "Bands" + str(mules) + "/" + str(run) + "/ALL/"
            print("\nALL -----------------------")

        elif ind == 1:
            S = [0]
            path_to_folder = "Bands" + str(mules) + "/" + str(run) + "/TV/"
            print("\nTV ----------------------  ")

        elif ind == 3:
            S = [1]
            path_to_folder = "Bands" + str(mules) + "/" + str(run) + "/ISM/"
            print("\nISM ------------------------ ")

        elif ind == 2:
            S = [2]
            path_to_folder = "Bands" + str(mules) + "/" + str(run) + "/LTE/"
            print("\nLTE ----------------------------")

        elif ind == 4:
            S = [3]
            path_to_folder = "Bands" + str(mules) + "/" + str(run) + "/CBRS/"
            print("\nCBRS --------------------------- ")

        # Set correct folder names
        link_exists_folder = "Bands" + str(mules) + "/" + str(run) + "/"
        lex_data_directory = "Lexington" + str(mules) + "/" + str(run) + "/"
        lex_data_directory_day = "Lexington" + str(mules) + "/" + str(run) + "/Day1/"
        validate_data_directory = "Lexington" + str(mules) + "/" + str(run) + "/Day1/"

        with open("constants.py", "r") as f:
            lines = f.readlines()

        with open("constants.py", "w") as f:
            for line in lines:
                if ("path_to_folder" not in line) and ("S = " not in line) and (
                    "validate_data_directory" not in line) \
                        and ("link_exists_folder" not in line) and ("lex_data_directory" not in line) \
                        and ("V = " not in line) and ("NoOfDMs = " not in line) and ("T =" not in line):
                    f.write(line)

            f.write("T = " + str(T) + "\n")
            f.write("V = " + str(mules + 12) + "\n")
            f.write("NoOfDMs = " + str(mules) + "\n")
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
    max_nodes = 50
    #mule_set = [65]
    # mule_set = [50, 0, 45, 40, 35, 30, 25, 15, 10, 5]
    mule_set = [50, 0, 1, 35, 30, 25, 20, 15, 10, 5, 2, 3]
    for max_mules in mule_set:
        for run in range(1, 6):
            print("=============== Folder: Band" + str(max_mules) + " Round: " + str(run))

            S = [0, 1, 2, 3]
            path_to_folder = "Bands" + str(max_mules) + "/" + str(run) + "/ALL/"
            link_exists_folder = "Bands" + str(max_mules) + "/" + str(run) +"/"
            lex_data_directory = "Lexington" + str(max_mules) + "/" + str(run) +"/"
            lex_data_directory_day = "Lexington" + str(max_mules) + "/" + str(run) + "/Day1/"

            if max_mules == 25:
                T = 60
            else:
                T = 30

            if set_max_nodes == True:
                # max_nodes = max_mules
                set_max_nodes = False

            with open("constants.py", "r") as f:
                lines = f.readlines()

            with open("constants.py", "w") as f:
                for line in lines:
                    if ("path_to_folder" not in line) and ("S = " not in line) \
                            and ("link_exists_folder" not in line) and ("lex_data_directory" not in line) \
                            and ("V = " not in line) and ("NoOfDMs = " not in line) and ("T = " not in line) \
                            and ("max_nodes = " not in line):
                        f.write(line)
                
                f.write("max_nodes = " + str(max_nodes) + "\n")
                f.write("T = " + str(T) + "\n")
                f.write("V = " + str(max_mules + 12) + "\n")
                f.write("NoOfDMs = " + str(max_mules) + "\n")
                f.write("path_to_folder = '" + str(path_to_folder) + "'\n")
                f.write("S = " + str(S) + "\n")
                f.write("lex_data_directory = '" + str(lex_data_directory) + "'\n")
                f.write("lex_data_directory_day = '" + str(lex_data_directory_day) + "'\n")
                f.write("link_exists_folder = '" + str(link_exists_folder) + "'\n")

            os.system('python3 readLexingtonData.py')
            os.system('python3 computeLINKEXISTS.py')

            run_simulation_files(max_mules, T, max_nodes, run)

else:
    print("\n================ Trajectory files were NOT regenerated. \n")

#run_simulation = input("Do you want to run the simulation?Y/N  ")


'''
number_of_runs = 2
run_simulation = "Y"
#TODO: Run the simulation
if run_simulation == "Y":
    for mules in range(5, 20, 10):
        for ind in range(0, 2):
            for run in range(1, 4):

                if ind == 0:
                    S = [0, 1, 2, 3]
                    path_to_folder = "Bands" + str(mules) + "/" + str(run) + "/ALL/"
                    print("ALL -----------------------\n")

                elif ind == 1:
                    S = [0]
                    path_to_folder = "Bands" + str(mules) + "/" + str(run) + "/TV/"
                    print("TV ----------------------  \n")

                elif ind == 3:
                    S = [1]
                    path_to_folder = "Bands" + str(mules) + "/" + str(run) + "/ISM/"
                    print("ISM ------------------------ \n")

                elif ind == 2:
                    S = [2]
                    path_to_folder = "Bands" + str(mules) + "/" + str(run) + "/LTE/"
                    print("LTE ----------------------------\n")

                elif ind == 4:
                    S = [3]
                    path_to_folder = "Bands" + str(mules) + "/" + str(run) + "/CBRS/"
                    print("CBRS --------------------------- \n")


                #Set correct folder names
                link_exists_folder = "Bands" + str(mules) + "/" + str(run) + "/"
                lex_data_directory = "Lexington" + str(mules) + "/" + str(run) + "/"
                lex_data_directory_day = "Lexington" + str(mules) + "/" + str(run) + "/Day1/"
                validate_data_directory = "Lexington" + str(mules) + "/" + str(run) + "/Day1/"
                
                #Set simulation time
                
                T = 45
               
                    
                with open("constants.py", "r") as f:
                    lines = f.readlines()

                with open("constants.py", "w") as f:
                    for line in lines:
                        if ("path_to_folder" not in line) and ("S = " not in line) and ("validate_data_directory" not in line) \
                                and ("link_exists_folder" not in line) and ("lex_data_directory" not in line) \
                                and ("V = " not in line) and ("NoOfDMs = " not in line) and ("T =" not in line):
                            f.write(line)
                    
                    f.write("T = " + str(T) + "\n")
                    f.write("V = " + str(mules + 10) + "\n")
                    f.write("NoOfDMs = " + str(mules) + "\n")
                    f.write("path_to_folder = '" + str(path_to_folder) + "'\n")
                    f.write("S = " + str(S) + "\n")
                    f.write("validate_data_directory = '" + str(validate_data_directory) + "'\n")
                    f.write("lex_data_directory = '" + str(lex_data_directory) + "'\n")
                    f.write("lex_data_directory_day = '" + str(lex_data_directory_day) + "'\n")
                    f.write("link_exists_folder = '" + str(link_exists_folder) + "'\n")


                print("Folder: Band" + str(mules) + " Band Type: " + str(ind) + " Round: " + str(run))

                os.system('python3 STB_main_path.py')
                os.system('python3 main2.py')
                os.system('python3 metrics.py')


else:
    print("\n================== Simulation was NOT run.")
'''