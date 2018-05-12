import os

#Take some inputs
#number_of_runs = input("Input number of runs?  ")
#generate_files = input("Do you want to generate the trajectory files?Y/N  ")

def run_simulation_files():

    for ind in range(5):
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
        # if ind == 0:
        #    os.system('python3 computeLINKEXISTS_UMass.py')

        os.system('python3 STB_main_path.py')
        # if ind == 0:
        #     os.system('python3 generateMessage_new.py')
        os.system('python3 main2.py')
        os.system('python3 metrics.py')


#main
# os.system('python3 createSrcDst.py')
run_simulation_files()
os.system('python3 plot_UMass.py')

