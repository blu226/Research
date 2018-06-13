import numpy as np
import matplotlib.pyplot as plt
from STB_help import *


#TODO: This is the number of nodes [10, 20, 30, 40, 50]
time_epochs = 4 #No of nodes
runs = 3
days = 4
#4 time stamps (15,30,45,60) and 10 runs
ALL = np.zeros(shape=(days, time_epochs,runs))
# LTE = np.zeros(shape=(days, time_epochs,runs))
# TV = np.zeros(shape=(days, time_epochs,runs))
# CBRS = np.zeros(shape=(days, time_epochs,runs))
# ISM = np.zeros(shape=(days, time_epochs,runs))

#folder_names = ["Bands0/", "Bands1/", "Bands3/", "Bands5/", "Bands10/", "Bands15/", "Bands20/", "Bands25/", "Bands30/", "Bands50/"]
folder_names = ["Bands5/","Bands15/", "Bands25/",  "Bands35/"]
file_names = ["metrics_LLC_day1.txt", "metrics_LLC_day2.txt", "metrics_LLC_day3.txt", "metrics_LLC_day4.txt"]
p_id = 1 #p_id = 1 for PDR, = 2 for latency, and 3 for Energy


#TODO: Here t is the number of nodes
t = 0
#For each set of nodes
for folder_name in folder_names:
    folders = os.listdir(folder_name)
    folders.sort()
    # folders = ["1", "2", "3", "4", "5"]
    # print("Folders: ", folders)

    #For each run
    for f_id in range(runs):
        # print("============= Current folder ", folder_name, " ", folders[f_id])
        band_type_folders = os.listdir(folder_name + folders[f_id])

        #For each band type
        for bt_id in range(1):
            if os.path.isdir(folder_name + folders[f_id] +"/" + band_type_folders[bt_id]):

                for day_id in range(len(file_names)):
                    # if "ALL" in band_type_folders[bt_id]:
                    f = open(folder_name + folders[f_id] + "/" + band_type_folders[bt_id] + "/" + file_names[day_id], "r")
                    lines = f.readlines()[1:]

                    for line in lines:
                        line_arr = line.strip().split("\t")
                        if "90" in line_arr[0]:

                            if "ALL" in band_type_folders[bt_id]:
                                # print(line_arr[0], " ", line_arr[p_id].split(" ")[0])
                                ALL[day_id][t][f_id] = line_arr[p_id].split(" ")[0]

                            # elif "TV" in band_type_folders[bt_id]:
                            #     TV[t][f_id] = line_arr[p_id].split(" ")[0]
                            #
                            # elif "CBRS" in band_type_folders[bt_id]:
                            #     CBRS[t][f_id] = line_arr[p_id].split(" ")[0]
                            #
                            # elif "ISM" in band_type_folders[bt_id]:
                            #     ISM[t][f_id] = line_arr[p_id].split(" ")[0]
                            #
                            # elif "LTE" in band_type_folders[bt_id]:
                            #     LTE[t][f_id] = line_arr[p_id].split(" ")[0]

    t += 1



#TODO: Plot the graph now
ALL_mean = [[None for _ in range(time_epochs)] for _ in range(days)]
ALL_SD =  [[None for _ in range(time_epochs)] for _ in range(days)]
# LTE_mean = []
# LTE_SD = []
# TV_mean = []
# TV_SD = []
# ISM_mean = []
# ISM_SD = []
# CBRS_mean = []
# CBRS_SD = []

print(ALL_SD[0])

for i in range(days):
    print("\n", " Node ", i, ALL[i])
    for j in range(time_epochs):
        # print("\n", " Node ", i, ALL[i][j])
        #print(TV[i])
        # print("Mean: ", np.mean(ALL[i][j]))
        # print("STD: ", np.std(ALL[i][j]))
        ALL_mean[i][j] = np.mean(ALL[i][j])
        ALL_SD[i][j] = np.std(ALL[i][j])
        # LTE_mean.append(np.mean(LTE[i]))
        # LTE_SD.append(np.std(LTE[i]))
        # TV_mean.append(np.mean(TV[i]))
        # TV_SD.append(np.std(TV[i]))
        # ISM_mean.append(np.mean(ISM[i]))
        # ISM_SD.append(np.std(ISM[i]))
        # CBRS_mean.append(np.mean(CBRS[i]))
        # CBRS_SD.append(np.std(CBRS[i]))

print(ALL_SD[0])
print(ALL_SD[1])
#x = np.array([2, 5, 7, 10, 15, 20, 25, 30, 35, 40])
x = np.array([5, 15, 25, 35])
plt.xlim(3, 36)
plt.xticks(x)
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)

fig_name = "dummy.eps"
if p_id == 1:
    plt.ylabel('Packet delivery ratio',  fontsize=25)
    plt.xlabel('Number of nodes', fontsize=25)
    plt.ylim(-0.05, 1)
    # plt.xlim(0, 50)
    plt.yticks(fontsize=25)
    fig_name = "Plots/pdr_nodes_error_bars_day2.eps"

    # plt.errorbar(x, ALL_mean, [x * 0.5 for x in ALL_SD])
    # plt.errorbar(x, LTE_mean, [x * 0.5 for x in LTE_SD])
    # plt.errorbar(x, TV_mean, [x * 0.5 for x in TV_SD])
    # plt.errorbar(x, ISM_mean, [x * 0.5 for x in ISM_SD])
    # plt.errorbar(x, CBRS_mean, [x * 0.5 for x in CBRS_SD])


    # plt.errorbar(x, LTE_mean, [x for x in LTE_SD])
    # plt.errorbar(x, TV_mean, [x for x in TV_SD])
    # plt.errorbar(x, ISM_mean, [x for x in ISM_SD])
    # plt.errorbar(x, CBRS_mean, [x for x in CBRS_SD])

if p_id == 2:
    plt.ylabel('Latency (in minutes)',  fontsize=25)
    plt.xlabel('Number of nodes',  fontsize=25)
    plt.ylim(-0.5, 50)
    fig_name = "Plots/latency_nodes_error_bars_day2.eps"

    # plt.errorbar(x, [x * 2 for x in ALL_mean], [x * 0.5 for x in ALL_SD])
    # plt.errorbar(x, [x * 2 for x in LTE_mean], [x * 0.5 for x in LTE_SD])
    # plt.errorbar(x, [x * 2 for x in TV_mean], [x * 0.5 for x in TV_SD])
    # plt.errorbar(x, [x * 2 for x in ISM_mean], [x * 0.5 for x in ISM_SD])
    # plt.errorbar(x, [x * 2 for x in CBRS_mean], [x * 0.5 for x in CBRS_SD])

if p_id == 3:
    plt.ylabel('Energy consumed', fontsize=25)
    plt.xlabel('Simulation time', fontsize=25)
    fig_name = "Plots/energy_nodes_error_bars_day2.eps"

    # plt.errorbar(x, ALL_mean, [x * 0.5 for x in ALL_SD])
    # plt.errorbar(x, LTE_mean, [x * 0.5 for x in LTE_SD])
    # plt.errorbar(x, TV_mean, [x * 0.5 for x in TV_SD])
    # plt.errorbar(x, ISM_mean, [x * 0.5 for x in ISM_SD])
    # plt.errorbar(x, CBRS_mean, [x * 0.5 for x in CBRS_SD])

# for i in range(days):
#     plt.errorbar(x, ALL_mean[i], [x for x in ALL_SD[i]])
    #plt.errorbar(x, ALL_mean[1], [x for x in ALL_SD[1]])

plt.errorbar(x, ALL_mean[0], ALL_SD[0],  marker='o', linestyle='-', linewidth=2)
plt.errorbar(x, ALL_mean[1], ALL_SD[1],  marker='*', linestyle='--', linewidth=2)
plt.errorbar(x, ALL_mean[2], ALL_SD[2],  marker='^', linestyle=':', linewidth=2 )
plt.errorbar(x, ALL_mean[3], ALL_SD[3], marker='s', linestyle='-.', linewidth=2)

plt.legend(['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5'], loc = "lower right", ncol = 1, fontsize = 20)

plt.tight_layout()
plt.savefig(fig_name)

plt.show()



                    # # Enter in the raw data
    # aluminum = np.array([6.4e-5 , 3.01e-5 , 2.36e-5, 3.0e-5, 7.0e-5, 4.5e-5, 3.8e-5, 4.2e-5, 2.62e-5, 3.6e-5])
    # copper = np.array([4.5e-5 , 1.97e-5 , 1.6e-5, 1.97e-5, 4.0e-5, 2.4e-5, 1.9e-5, 2.41e-5 , 1.85e-5, 3.3e-5 ])
    # steel = np.array([3.3e-5 , 1.2e-5 , 0.9e-5, 1.2e-5, 1.3e-5, 1.6e-5, 1.4e-5, 1.58e-5, 1.32e-5 , 2.1e-5])
    #
    #
    # # Calculate the average
    # aluminum_mean = np.mean(aluminum)
    # copper_mean = np.mean(copper)
    # steel_mean = np.mean(steel)
    #
    # aluminum_std = np.std(aluminum)
    # copper_std = np.std(copper)
    # steel_std = np.std(steel)
    #
    # # Create Arrays for the plot
    # materials = ['Aluminum', 'Copper', 'Steel']
    # x_pos = np.arange(len(materials))
    # CTEs = [aluminum_mean, copper_mean, steel_mean]
    # error = [aluminum_std, copper_std, steel_std]
    #
    # # Build the plot
    # fig, ax = plt.subplots()
    # ax.bar(x_pos, CTEs, yerr=error, align='center', alpha=0.5, ecolor='black', capsize=10)
    # ax.set_ylabel('Coefficient of Thermal Expansion ($\degree C^{-1}$)')
    # ax.set_xticks(x_pos)
    # ax.set_xticklabels(materials)
    # ax.set_title('Coefficent of Thermal Expansion (CTE) of Three Metals')
    # ax.yaxis.grid(True)
    #
    # # Save the figure and show
    # plt.tight_layout()
    # plt.savefig('bar_plot_with_error_bars.png')
    # plt.show()