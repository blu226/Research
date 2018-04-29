import os

#Take some inputs
#number_of_runs = input("Input number of runs?  ")
#generate_files = input("Do you want to generate the trajectory files?Y/N  ")

number_of_runs = 1

'''
generate_files = "Y"
# generate_files = "N"
#TODO: Generate the trajectory files
if generate_files == "Y":
    print("Generate bus trajectories ---------------------- \n")
    for mule in range(10, 60, 10):
        for run in range(1, 11):
            print("=============== Folder: Band" + str(mule) + " Round: " + str(run))

            S = [0, 1, 2, 3]
            path_to_folder = "Bands" + str(mule) + "/" + str(run) + "/ALL/"
            link_exists_folder = "Bands" + str(mule) + "/" + str(run) +"/"
            lex_data_directory = "Lexington" + str(mule) + "/" + str(run) +"/"
            lex_data_directory_day = "Lexington" + str(mule) + "/" + str(run) + "/Day1/"

            if mule == 30:
                T = 120
            else:
                T = 60

            with open("constants.py", "r") as f:
                lines = f.readlines()

            with open("constants.py", "w") as f:
                for line in lines:
                    if ("path_to_folder" not in line) and ("S = " not in line) \
                            and ("link_exists_folder" not in line) and ("lex_data_directory" not in line) \
                            and ("V = " not in line) and ("NoOfDMs = " not in line) and ("T = " not in line):
                        f.write(line)
                f.write("T = " + str(T) + "\n")
                f.write("V = " + str(mule + 15) + "\n")
                f.write("NoOfDMs = " + str(mule) + "\n")
                f.write("path_to_folder = '" + str(path_to_folder) + "'\n")
                f.write("S = " + str(S) + "\n")
                f.write("lex_data_directory = '" + str(lex_data_directory) + "'\n")
                f.write("lex_data_directory_day = '" + str(lex_data_directory_day) + "'\n")
                f.write("link_exists_folder = '" + str(link_exists_folder) + "'\n")

            os.system('python3 readLexingtonData.py')
            os.system('python3 computeLINKEXISTS.py')

else:
    print("\n================ Trajectory files were NOT regenerated. \n")



'''

#run_simulation = input("Do you want to run the simulation?Y/N  ")

number_of_runs = 2
run_simulation = "Y"
#TODO: Run the simulation
if run_simulation == "Y":
    for mules in range(10, 60, 10):
        for ind in range(0, 5):
            for run in range(1, 11):

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
                if mules == 30:
                    T = 60
                else:
                    T = 60
                    
                with open("constants.py", "r") as f:
                    lines = f.readlines()

                with open("constants.py", "w") as f:
                    for line in lines:
                        if ("path_to_folder" not in line) and ("S = " not in line) and ("validate_data_directory" not in line) \
                                and ("link_exists_folder" not in line) and ("lex_data_directory" not in line) \
                                and ("V = " not in line) and ("NoOfDMs = " not in line) and ("T =" not in line):
                            f.write(line)
                    
                    f.write("T = " + str(T) + "\n")
                    f.write("V = " + str(mules + 15) + "\n")
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

