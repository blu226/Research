import os

generate_files = True

if generate_files == True:
    print("Generate bus trajectories ---------------------- \n")
    for run in range(1,2):
        print("Round: " + str(run))

        link_exists_folder = "Bands/" + str(run) +"/"
        lex_data_directory = "Lexington/" + str(run) +"/"
        lex_data_directory_day = "Lexington/" + str(run) + "/Day1/"

        with open("constants.py", "r") as f:
            lines = f.readlines()

        with open("constants.py", "w") as f:
            for line in lines:
                if ("link_exists_folder" not in line and "lex_data_directory" not in line):
                    f.write(line)

            f.write("lex_data_directory = '" + str(lex_data_directory) + "'\n")
            f.write("lex_data_directory_day = '" + str(lex_data_directory_day) + "'\n")
            f.write("link_exists_folder = '" + str(link_exists_folder) + "'\n")

        os.system('python3 readLexingtonData.py')
        os.system('python3 computeLINKEXISTS.py')

run_simulation = False

if run_simulation == True:
    for ind in range(0, 5):
        for run in range(1, 3):

            if ind == 0:
                S = [0, 1, 2, 3]
                path_to_folder = "Bands/" + str(run) + "/ALL/"
                print("ALL -----------------------\n")

            elif ind == 1:
                S = [0]
                path_to_folder = "Bands/" + str(run) + "/TV/"
                print("TV ----------------------  \n")

            elif ind == 3:
                S = [1]
                path_to_folder =  "Bands/" + str(run) + "/ISM/"
                print("ISM ------------------------ \n")

            elif ind == 2:
                S = [2]
                path_to_folder =   "Bands/" + str(run) + "/LTE/"
                print("LTE ----------------------------\n")

            elif ind == 4:
                S = [3]
                path_to_folder =   "Bands/" + str(run) + "/CBRS/"
                print("CBRS --------------------------- \n")


            with open("constants.py", "r") as f:
                lines = f.readlines()

            with open("constants.py", "w") as f:
                for line in lines:
                    if ("path_to_folder" not in line and "S = " not in line and "link_exists_folder" not in line):
                        f.write(line)

                f.write("path_to_folder = '" + str(path_to_folder) + "'\n")
                f.write("S = " + str(S) + "\n")
                f.write("link_exists_folder = '" + str(link_exists_folder) + "'\n")

            print("Round: " + str(run))

            os.system('python3 STB_main_path.py')
            os.system('python3 main2.py')
            os.system('python3 metrics.py')

