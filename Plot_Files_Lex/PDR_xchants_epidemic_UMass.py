import numpy as np
import os
import matplotlib.pyplot as plt

time_epochs = 9
runs = 1
# 4 time stamps (15,30,45,60) and 10 runs
Xchants = np.zeros(shape=(time_epochs,runs))
Xchants_pk = np.zeros(shape=(time_epochs,runs))

Epidemic_ALL = np.zeros(shape=(time_epochs,runs))
Epidemic_LTE = np.zeros(shape=(time_epochs,runs))
Epidemic_TV = np.zeros(shape=(time_epochs,runs))
Epidemic_CBRS = np.zeros(shape=(time_epochs,runs))
Epidemic_ISM = np.zeros(shape=(time_epochs,runs))

# routing_paths = ["../Bands_UMass18/2007-10-23", "../Bands_UMass16/2007-10-24", "../Bands_UMass20/2007-10-31", "../Bands_UMass21/2007-11-01", "../Bands_UMass23/2007-11-06", "../Bands_UMass16/2007-11-07"]
routing_paths = ["../Bands_UMass20/2007-11-07"]
folder_name = ["../Bands_UMass20/"]
band_folders = ["ALL", "CBRS", "ISM", "LTE", "TV"]
V = 20
folders = os.listdir(folder_name[0])

p_id = 2 # p_id = 1 for PDR, = 2 for latency, and 3 for Energy, and 4 for overhead

folders.sort()
# folders = "1"
print("Folders: ", folders)

for routing_path in routing_paths:

    unique_fig_name_arr = routing_path.split('/')
    unique_fig_name = unique_fig_name_arr[2]
#Run - 1, 2, 3
    for run in range(runs):
        print("============= Current folder ", folders[run])

        #TODO: Fixed - Day2
        so_far_folder = routing_path + "/Day2/"
        # band_folders = os.listdir(so_far_folder)

        #Bands - ALL, LTE, ISM, ..
        for band in band_folders:
            routing_folders = os.listdir(so_far_folder + band)

            #Routing - XCHANTs, epidemic ...
            for routing_folder in routing_folders:
                lines = []
                metric_file = ""

                if "ALL" == band and "XChants" == routing_folder:
                    metric_file = open(so_far_folder + band + "/" + routing_folder + "/metrics_LLC_day2_X-CHANTS.txt")

                elif routing_folder == "Epidemic" :
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

t = 0
print("ALL", Epidemic_ALL)
metric_file = open("../Bands_UMass" + str(V) + "/2007-11-07/Day2/ALL/XChants/metrics_LLC_day2_X-CHANTS_opt.txt", "r")
lines = metric_file.readlines()[1:]
for line in lines:
    line_arr = line.strip().split("\t")
    Xchants_pk[t][run] = line_arr[p_id]

    if p_id == 3:
        Xchants_pk[t][run] = float(Xchants_pk[t][run])/1000
    t += 1

if p_id == 3:
    for t in range(len(Xchants)):
        for run in range(runs):
            Xchants[t][run] = float(Xchants[t][run]) / 1000
            Epidemic_ALL[t][run] = float(Epidemic_ALL[t][run]) / 1000
            Epidemic_CBRS[t][run] = float(Epidemic_CBRS[t][run]) / 1000
            Epidemic_ISM[t][run] = float(Epidemic_ISM[t][run]) / 1000
            Epidemic_LTE[t][run] = float(Epidemic_LTE[t][run]) / 1000
            Epidemic_TV[t][run] = float(Epidemic_TV[t][run]) / 1000

Xchants_mean = []
Xchants_SD = []
Xchants_mean_pk = []
Xchants_SD_pk = []
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

for i in range(len(Xchants)):
    Xchants_mean.append(np.mean(Xchants[i]))
    Xchants_SD.append(np.std(Xchants[i]))
    Xchants_mean_pk.append(np.mean(Xchants_pk[i]))
    Xchants_SD_pk.append(np.std(Xchants_pk[i]))
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

x = np.array([0,30, 60, 90, 120, 150, 180])
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
plt.xticks(np.arange(0, 190, step = 30))

fig_name = "dummy.eps"

if p_id == 1:
    plt.ylabel('Message Delivery Ratio', fontsize=25)
    plt.xlabel('Simulation time (min)', fontsize=25)
    # plt.ylim(0,1.2)
    # plt.xticks(np.arange(min(x), max(x) + 1, 15), fontsize = 20)
    plt.yticks(fontsize=25)
    # plt.xticks(np.arange(0, 190, step = 30))
    fig_name = "../Plots/pdr_time_UMass_" + unique_fig_name + ".eps"

if p_id == 2:
    # plt.ylim(0, 75)
    plt.ylabel('Network Delay (min)', fontsize=25)
    plt.xlabel('Simulation time (in minutes)', fontsize=25)
    # plt.xticks(np.arange(0, 250, step = 30))
    fig_name = "../Plots/latency_time_UMass_" + unique_fig_name + ".eps"

if p_id == 3:
    plt.ylabel('Energy Expenditure (KJ)', fontsize=25)
    plt.xlabel('Simulation time (in minutes)', fontsize=25)
    # plt.xticks(np.arange(0, 250, step = 30))
    fig_name = "../Plots/energy_time_UMass_" + unique_fig_name + ".eps"

if p_id == 4:
    plt.ylabel('Message Overhead', fontsize=25)
    plt.xlabel('Simulation time (in minutes)', fontsize=25)
    # plt.xticks(np.arange(0, 250, step = 30))
    fig_name = "../Plots/overhead_time_UMass_" + unique_fig_name + ".eps"


plt.errorbar(x, Xchants_mean_pk[:7], Xchants_SD_pk[:7], marker='o', linestyle='-', linewidth=2)
plt.errorbar(x, Xchants_mean[:7], Xchants_SD[:7], marker='o', linestyle='-', linewidth=2)
plt.errorbar(x, Epidemic_ALL_mean[:7], Epidemic_ALL_SD[:7], marker='*', linestyle='--', linewidth=2)
plt.errorbar(x, Epidemic_CBRS_mean[:7], Epidemic_CBRS_SD[:7], marker='^', linestyle=':', linewidth=2)
plt.errorbar(x, Epidemic_ISM_mean[:7], Epidemic_ISM_SD[:7], marker='D', linestyle='--', linewidth=2)
plt.errorbar(x, Epidemic_LTE_mean[:7], Epidemic_LTE_SD[:7], marker='s', linestyle='-.', linewidth=2)
plt.errorbar(x, Epidemic_TV_mean[:7], Epidemic_TV_SD[:7], marker='s', linestyle='-.', linewidth=2)

if p_id == 1:
    plt.legend(["X-CHANT (Ideal)","X-CHANT", "S-ER", "CBRS", "ISM", "LTE", "TV"], loc="upper left", fontsize=15, ncol = 1, frameon=False)
elif p_id == 2:
    plt.legend(["X-CHANT (Ideal)", "X-CHANT", "S-ER", "CBRS", "ISM", "LTE", "TV"], loc="upper left", fontsize=15,ncol=1, frameon=False)
elif p_id == 3:
    plt.legend(["X-CHANT (Ideal)", "X-CHANT", "S-ER", "CBRS", "ISM", "LTE", "TV"], loc="upper left", fontsize=15,ncol=1, frameon=False)
elif p_id == 4:
    plt.legend(["X-CHANT (Ideal)", "X-CHANT", "S-ER", "CBRS", "ISM", "LTE", "TV"], loc="upper left", fontsize=15, ncol=1, frameon=False)

plt.tight_layout()
plt.savefig(fig_name)

plt.show()
