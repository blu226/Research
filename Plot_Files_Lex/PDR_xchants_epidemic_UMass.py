import numpy as np
import os
import matplotlib.pyplot as plt

time_epochs = 13
runs = 1
# 4 time stamps (15,30,45,60) and 10 runs
Xchants = np.zeros(shape=(time_epochs,runs))
Epidemic_ALL = np.zeros(shape=(time_epochs,runs))
Epidemic_LTE = np.zeros(shape=(time_epochs,runs))
Epidemic_TV = np.zeros(shape=(time_epochs,runs))
Epidemic_CBRS = np.zeros(shape=(time_epochs,runs))
Epidemic_ISM = np.zeros(shape=(time_epochs,runs))


folder_name = ["../Bands_UMass23/"]
band_folders = ["ALL", "CBRS", "ISM", "LTE", "TV"]

folders = os.listdir(folder_name[0])

p_id = 4  # p_id = 1 for PDR, = 2 for latency, and 3 for Energy, and 4 for overhead

folders.sort()
# folders = "1"
print("Folders: ", folders)

#Run - 1, 2, 3
for run in range(runs):
    print("============= Current folder ", folders[run])

    #TODO: Fixed - Day2
    so_far_folder = folder_name[0] + folders[run] + "/" + "Day2/"
    # band_folders = os.listdir(so_far_folder)

    print("Band folders: ", band_folders)
    #Bands - ALL, LTE, ISM, ..
    for band in band_folders:
        routing_folders = os.listdir(so_far_folder + band)
        print("Routing folders: ", routing_folders)

        #Routing - XCHANTs, epidemic ...
        for routing_folder in routing_folders:
            lines = []
            metric_file = ""

            if "ALL" == band and "XChants" == routing_folder:
                metric_file = open(so_far_folder + band + "/" + routing_folder + "/metrics_LLC_day2_X-CHANTS.txt")

            elif routing_folder == "Epidemic" and band != "ALL":
                metric_file = open(so_far_folder + band + "/" + routing_folder + "/metrics_LLC_day2_Epi.txt")

            if metric_file != "":
                lines = metric_file.readlines()[1:]

            print("Run: ", folders[run], " Band: ", band, " routing: ", str(routing_folder), lines)

            t = 0
            for line in lines:
                line_arr = line.strip().split("\t")

                if "XChants" == routing_folder:
                    if "ALL" == band:
                        Xchants[t][run] = line_arr[p_id]

                elif "Epidemic" == routing_folder:
                    if "ALL" == band:
                        Epidemic_ALL[t][run] = line_arr[p_id]

                    if "CBRS" == band:
                        Epidemic_CBRS[t][run] = line_arr[p_id]

                    if "ISM" == band:
                        Epidemic_ISM[t][run] = line_arr[p_id]

                    if "LTE" == band:
                        Epidemic_LTE[t][run] = line_arr[p_id]

                    if "TV" == band:
                        Epidemic_TV[t][run] = line_arr[p_id]
                t = t + 1

Xchants_mean = []
Xchants_SD = []
Epidemic_ALL_mean = []
Epidemic_ALL_SD = []
Epidemic_CBRS_mean = []
Epidemic_CBRS_SD = []
Epidemic_ISM_mean = []
Epidemic_ISM_SD = []
Epidemic_LTE_mean = []
Epidemic_LTE_SD = []
Epidemic_TV_mean = []
Epidemic_TV_SD = []

print(Epidemic_ISM)
for i in range(len(Xchants)):
    Xchants_mean.append(np.mean(Xchants[i]))
    Xchants_SD.append(np.std(Xchants[i]))
    Epidemic_ALL_mean.append(np.mean(Epidemic_ALL[i]))
    Epidemic_ALL_SD.append(np.std(Epidemic_ALL[i]))
    Epidemic_CBRS_mean.append(np.mean(Epidemic_CBRS[i]))
    Epidemic_CBRS_SD.append(np.std(Epidemic_CBRS[i]))
    Epidemic_ISM_mean.append(np.mean(Epidemic_ISM[i]))
    Epidemic_ISM_SD.append(np.std(Epidemic_ISM[i]))
    Epidemic_LTE_mean.append(np.mean(Epidemic_LTE[i]))
    Epidemic_LTE_SD.append(np.std(Epidemic_LTE[i]))
    Epidemic_TV_mean.append(np.mean(Epidemic_TV[i]))
    Epidemic_TV_SD.append(np.std(Epidemic_TV[i]))

x = np.array([0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180])
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)

fig_name = "dummy.eps"

if p_id == 1:
    plt.ylabel('Packet delivery ratio', fontsize=25)
    plt.xlabel('Simulation time (in minutes)', fontsize=25)
    plt.yticks(fontsize=25)
    fig_name = "../Plots/pdr_time_UMass.eps"

if p_id == 2:
    plt.ylim(0, 60)
    plt.ylabel('Latency (in minutes)', fontsize=25)
    plt.xlabel('Simulation time (in minutes)', fontsize=25)
    fig_name = "../Plots/latency_time_UMass.eps"


if p_id == 4:
    plt.ylabel('Message overhead', fontsize=25)
    plt.xlabel('Simulation time (in minutes)', fontsize=25)
    fig_name = "../Plots/overhead_time_UMass.eps"



plt.errorbar(x, Xchants_mean, Xchants_SD, marker='o', linestyle='-', linewidth=2)
# plt.errorbar(x, Epidemic_ALL_mean, Epidemic_ALL_SD, marker='*', linestyle='--', linewidth=2)
plt.errorbar(x, Epidemic_CBRS_mean, Epidemic_CBRS_SD, marker='^', linestyle=':', linewidth=2)
plt.errorbar(x, Epidemic_ISM_mean, Epidemic_ISM_SD, marker='D', linestyle='--', linewidth=2)
plt.errorbar(x, Epidemic_LTE_mean, Epidemic_LTE_SD, marker='s', linestyle='-.', linewidth=2)
plt.errorbar(x, Epidemic_TV_mean, Epidemic_TV_SD, marker='s', linestyle='-.', linewidth=2)

if p_id == 1:
    plt.legend(["X-CHANTs", "CBRS", "ISM", "LTE", "TV"], loc="upper left", fontsize=17)
elif p_id == 2:
    plt.legend(["X-CHANTs", "CBRS", "ISM", "LTE", "TV"], loc="upper left", fontsize=18, ncol=2)
elif p_id == 4:
    plt.legend(["X-CHANTs", "CBRS", "ISM", "LTE", "TV"], loc="upper left", fontsize=18, ncol=2)


plt.tight_layout()
plt.savefig(fig_name)

plt.show()
