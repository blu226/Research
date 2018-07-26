import numpy as np
import os
import matplotlib.pyplot as plt

time_epochs = 5
# 4 time stamps (15,30,45,60) and 10 runs
Xchants = np.zeros(shape=(time_epochs,runs))
Xchants_pk = np.zeros(shape=(time_epochs,runs))
SprayNWait_ALL = np.zeros(shape=(time_epochs,runs))
HotPotato_ALL = np.zeros(shape=(time_epochs,runs))
Epidemic_ALL = np.zeros(shape=(time_epochs,runs))
SprayNWait5_ALL = np.zeros(shape=(time_epochs,runs))


folder_names = ["../Bands_UMass12/", "../Bands_UMass14/", "../Bands_UMass16/", "../Bands_UMass18/", "../Bands_UMass20/"]
band_folders = ["ALL"]
p_id = 4  # p_id = 1 for PDR, = 2 for latency, and 3 for Energy, and 4 for overhead

t = 0
for folder_name in folder_names:
    folder_day = "2007-11-07"

    #Run - 1, 2, 3
    for run in range(runs):
        # print("============= Current folder ", folders[run])

        #TODO: Fixed - Day2
        so_far_folder = folder_name + folder_day + "/" + "Day2/"
        print("Current Path: ", so_far_folder)
        # band_folders = os.listdir(so_far_folder)

        #Bands - ALL, LTE, ISM, ..
        for band in band_folders:
            routing_folders = os.listdir(so_far_folder + band)

            #Routing - XCHANTs, epidemic ...
            for routing_folder in routing_folders:

                lines = []
                metric_file = ""

                if "ALL" == band and "XChants" == routing_folder:
                    metric_file = open(so_far_folder + "/" + band + "/" + routing_folder + "/metrics_LLC_day2_X-CHANTS.txt")

                elif routing_folder == "Epidemic":
                    metric_file = open(so_far_folder + band + "/" + routing_folder + "/metrics_LLC_day2_Epi.txt")

                elif routing_folder == "SprayNWait":
                    metric_file = open(so_far_folder + band + "/" + routing_folder + "/metrics_LLC_day2_SnW.txt")

                elif routing_folder == "SprayNWait5":
                    metric_file = open(so_far_folder + band + "/" + routing_folder + "/metrics_LLC_day2_SnW.txt")

                elif routing_folder == "HotPotato":
                    metric_file = open(so_far_folder + band + "/" + routing_folder + "/metrics_LLC_day2_HP.txt")

                if metric_file != "":
                    lines = metric_file.readlines()[1:]

                print(" Band: ", band, " routing: ", str(routing_folder), lines)

                for line in lines:
                    line_arr = line.strip().split("\t")

                    if "180" in line_arr[0]:
                        if "XChants" == routing_folder:
                            if "ALL" == band:
                                Xchants[t][run] = line_arr[p_id]

                        elif "Epidemic" == routing_folder:
                            if "ALL" == band:
                                Epidemic_ALL[t][run] = line_arr[p_id]

                        elif "SprayNWait" == routing_folder:
                            if "ALL" == band:
                                SprayNWait_ALL[t][run] = line_arr[p_id]

                        elif "SprayNWait5" == routing_folder:
                            if "ALL" == band:
                                SprayNWait5_ALL[t][run] = line_arr[p_id]

                        elif "HotPotato" == routing_folder:
                            if "ALL" == band:
                                print()
                                HotPotato_ALL[t][run] = line_arr[p_id]


    t = t + 1

t = 0
folder_nums = [12, 14, 16, 18, 20]
for num_mules in folder_nums:
    metric_file = open("../Bands_UMass" + str(num_mules) +"/2007-11-07/Day2/ALL/XChants/metrics_LLC_day2_X-CHANTS_opt.txt", "r")
    lines = metric_file.readlines()[1:]
    for line in lines:
        line_arr = line.strip().split("\t")

        if "180" in line_arr[0]:

            Xchants_pk[t][run] = line_arr[p_id]

    t += 1
if p_id == 3:
    for t in range(len(Xchants)):
        for run in range(runs):
            Xchants[t][run] = float(Xchants[t][run]) / 1000
            Xchants_pk[t][run] = float(Xchants_pk[t][run])/1000
            Epidemic_ALL[t][run] = float(Epidemic_ALL[t][run]) / 1000
            SprayNWait_ALL[t][run] = float(SprayNWait_ALL[t][run])/1000
            SprayNWait5_ALL[t][run] = float(SprayNWait5_ALL[t][run]) / 1000
            HotPotato_ALL[t][run] = float(HotPotato_ALL[t][run])/1000
Xchants_mean = []
Xchants_SD = []
Xchants_mean_pk = []
Xchants_SD_pk = []
SprayNWait_ALL_mean = []
SprayNWait5_ALL_mean = []
HotPotato_ALL_mean = []
Epidemic_ALL_mean = []
Epidemic_ALL_SD = []


for i in range(len(Xchants)):
    Xchants_mean.append(np.mean(Xchants[i]))
    Xchants_SD.append(np.std(Xchants[i]))
    Xchants_mean_pk.append(np.mean(Xchants_pk[i]))
    Xchants_SD_pk.append(np.std(Xchants_pk[i]))
    SprayNWait_ALL_mean.append(np.mean(SprayNWait_ALL[i]))
    SprayNWait5_ALL_mean.append(np.mean(SprayNWait5_ALL[i]))
    HotPotato_ALL_mean.append(np.mean(HotPotato_ALL[i]))
    Epidemic_ALL_mean.append(np.mean(Epidemic_ALL[i]))
    Epidemic_ALL_SD.append(np.std(Epidemic_ALL[i]))


x = np.array([3, 5, 7, 9, 11])
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
plt.xticks(np.arange(3, 15, step=2))

fig_name = "dummy.eps"

if p_id == 1:
    plt.ylabel('Packet delivery ratio', fontsize=25)
    plt.xlabel('Number of Buses', fontsize=25)
    plt.ylim(0,1.05)
    plt.yticks(fontsize=25)
    fig_name = "../Plots/routing_pdr_nodes_UMass.eps"

if p_id == 2:
    plt.ylabel('Latency (min)', fontsize=25)
    plt.xlabel('Number of Buses', fontsize=25)
    # plt.ylim(0,55)
    fig_name = "../Plots/routing_latency_nodes_UMass.eps"

if p_id == 3:
    plt.ylabel('Energy Expenditure (KJ)', fontsize=25)
    plt.xlabel('Number of Buses', fontsize=25)
    # plt.ylim(0,3600)

    fig_name = "../Plots/routing_energy_nodes_UMass.eps"


if p_id == 4:
    plt.ylabel('Message overhead', fontsize=25)
    plt.xlabel('Number of Buses', fontsize=25)
    fig_name = "../Plots/routing_overhead_nodes_UMass.eps"


plt.errorbar(x, Xchants_mean_pk, Xchants_SD_pk, marker='o', linestyle='-', linewidth=2)
plt.errorbar(x, Xchants_mean, Xchants_SD, marker='o', linestyle='--', linewidth=2)
plt.errorbar(x, Epidemic_ALL_mean, Epidemic_ALL_SD, marker='^', linestyle='--', linewidth=2)
plt.errorbar(x, SprayNWait_ALL_mean, Epidemic_ALL_SD, marker='*', linestyle='--', linewidth=2)
# plt.errorbar(x, SprayNWait5_ALL_mean, Epidemic_ALL_SD, marker='*', linestyle='--', linewidth=2)
plt.errorbar(x, HotPotato_ALL_mean, Epidemic_ALL_SD, marker='^', linestyle='--', linewidth=2)


if p_id == 1:
    plt.legend(["X-CHANTS (Ideal)", "X-CHANTS", "S-ER", "S-SnW (25)", "S-HP"], loc="lower center", fontsize=15, ncol = 2, frameon=False)
elif p_id == 2:
    plt.legend(["X-CHANTS (Ideal)", "X-CHANTS", "S-ER", "S-SnW (25)", "S-HP"], loc="lower center", fontsize=15, ncol = 2, frameon=False)
elif p_id ==3:
    plt.legend(["X-CHANTS (Ideal)", "X-CHANTS", "S-ER", "S-SnW (25)", "S-HP"], loc="lower center", fontsize=15, ncol = 2, frameon=False)
elif p_id ==4:
    plt.legend(["X-CHANTS (Ideal)", "X-CHANTS", "S-ER", "S-SnW (25)", "S-HP"], loc="lower center", fontsize=15, ncol = 2, frameon=False)


plt.tight_layout()
plt.savefig(fig_name)

plt.show()
