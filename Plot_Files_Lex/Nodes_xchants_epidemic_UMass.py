import numpy as np
import os
import matplotlib.pyplot as plt

time_epochs = 5
runs = 1
# 4 time stamps (15,30,45,60) and 10 runs
Xchants = np.zeros(shape=(time_epochs,runs))
Xchants_pk = np.zeros(shape=(time_epochs,runs))
Epidemic_ALL = np.zeros(shape=(time_epochs,runs))
Epidemic_LTE = np.zeros(shape=(time_epochs,runs))
Epidemic_TV = np.zeros(shape=(time_epochs,runs))
Epidemic_CBRS = np.zeros(shape=(time_epochs,runs))
Epidemic_ISM = np.zeros(shape=(time_epochs,runs))

folder_name = "../Bands_UMass"
folder_nums = [12, 14, 16, 18, 20]
band_folders = ["ALL", "TV", "ISM", "LTE", "CBRS"]
p_id = 4  # p_id = 1 for PDR, = 2 for latency, and 3 for Energy, and 4 for overhead

t = 0
for num_mules in folder_nums:

    full_folder_name = folder_name + str(num_mules) + '/2007-11-07/'
    folders = os.listdir(full_folder_name)
    folders.sort()

    #Run - 1, 2, 3
    for run in range(1,2):
        run -= 1

        #TODO: Fixed - Day2
        so_far_folder = full_folder_name + folders[run + 1] + "/"
        print("============= Current folder ", so_far_folder)

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
                    metric_file = open(so_far_folder + "/" + band + "/" + routing_folder + "/metrics_LLC_day2_X-CHANTS.txt")

                elif routing_folder == "Epidemic":
                    metric_file = open(so_far_folder + band + "/" + routing_folder + "/metrics_LLC_day2_Epi.txt")

                if metric_file != "":
                    lines = metric_file.readlines()[1:]

                print("Run: ", folders[run], " Band: ", band, " routing: ", str(routing_folder), lines)

                for line in lines:
                    line_arr = line.strip().split("\t")

                    if "180" in line_arr[0]:
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

x = np.array([3, 5, 7, 9, 11])
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
plt.xticks(np.arange(3, 15, step=2))

fig_name = "dummy.eps"

if p_id == 1:
    plt.ylabel('Message Delivery Ratio', fontsize=25)
    plt.xlabel('Number of Buses', fontsize=25)
    plt.ylim(0,1)
    plt.yticks(fontsize=25)
    # plt.xticks(np.arange(0, 15, step=2))
    fig_name = "../Plots/pdr_nodes_UMass.eps"

if p_id == 2:
    plt.ylabel('Network Delay (min)', fontsize=25)
    plt.xlabel('Number of Buses', fontsize=25)
    # plt.ylim(0, 130)
    # plt.xticks(np.arange(0, 15, step=2))
    fig_name = "../Plots/latency_nodes_UMass.eps"

if p_id == 3:
    plt.ylabel('Energy Expenditure (KJ)', fontsize=25)
    # plt.xticks(np.arange(0, 15, step=2))
    plt.xlabel('Number of Buses', fontsize=25)
    fig_name = "../Plots/energy_nodes_UMass.eps"


if p_id == 4:
    plt.ylabel('Message overhead', fontsize=25)
    plt.xlabel('Number of Buses', fontsize=25)
    # plt.xticks(np.arange(0, 15, step=2))
    fig_name = "../Plots/overhead_nodes_UMass.eps"


plt.errorbar(x, Xchants_mean_pk, Xchants_SD_pk, marker='o', linestyle='-', linewidth=2)
plt.errorbar(x, Xchants_mean, Xchants_SD, marker='o', linestyle='-', linewidth=2)
plt.errorbar(x, Epidemic_ALL_mean, Epidemic_ALL_SD, marker='*', linestyle='--', linewidth=2)
plt.errorbar(x, Epidemic_CBRS_mean, Epidemic_CBRS_SD, marker='^', linestyle=':', linewidth=2)
plt.errorbar(x, Epidemic_ISM_mean, Epidemic_ISM_SD, marker='D', linestyle='--', linewidth=2)
plt.errorbar(x, Epidemic_LTE_mean, Epidemic_LTE_SD, marker='s', linestyle='-.', linewidth=2)
plt.errorbar(x, Epidemic_TV_mean, Epidemic_TV_SD, marker='s', linestyle='-.', linewidth=2)
ax = plt.subplot(111)
if p_id == 1 :
    ax.legend(["X-CHANT (Ideal)","X-CHANT", "S-ER", "CBRS", "ISM", "LTE", "TV"], loc="upper center", bbox_to_anchor=(0.77, .65),fontsize=13, ncol = 1, frameon=False)
elif p_id == 2:
    ax.legend(["X-CHANT (Ideal)","X-CHANT", "S-ER", "CBRS", "ISM", "LTE", "TV"], loc="upper center", bbox_to_anchor=(0.2, 1.0),fontsize=14, ncol = 1, frameon=False)
elif p_id == 3:
    ax.legend(["X-CHANT (Ideal)","X-CHANT", "S-ER", "CBRS", "ISM", "LTE", "TV"], loc="upper center", bbox_to_anchor=(0.7, 0.3),fontsize=14, ncol = 2, frameon=False)
elif p_id ==4:
    ax.legend(["X-CHANT (Ideal)","X-CHANT", "S-ER", "CBRS", "ISM", "LTE", "TV"], loc="upper center", bbox_to_anchor=(0.2, 0.55),fontsize=13, ncol = 1, frameon=False)


plt.tight_layout()
plt.savefig(fig_name)

plt.show()
