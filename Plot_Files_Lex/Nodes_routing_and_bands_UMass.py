import numpy as np
import matplotlib.pyplot as plt



time_epochs = 6

Xchants = np.zeros(shape=(time_epochs))
Xchants_pk = np.zeros(shape=(time_epochs))
Epidemic_ALL = np.zeros(shape=(time_epochs))
Epidemic_LTE = np.zeros(shape=(time_epochs))
Epidemic_TV = np.zeros(shape=(time_epochs))
Epidemic_CBRS = np.zeros(shape=(time_epochs))
Epidemic_ISM = np.zeros(shape=(time_epochs))
SprayNWait_ALL = np.zeros(shape=(time_epochs))
HotPotato_ALL = np.zeros(shape=(time_epochs))
Epidemic_ALL = np.zeros(shape=(time_epochs))

day = "2007-11-07"
folder_nums = [11, 13, 15,17, 19, 21]
bands = ["ALL", "LTE", "TV", "CBRS", "ISM"]
protocols = ["XChants", "Epidemic", "SprayNWait", "HotPotato"]

p_id = 0 # p_id = 1 for PDR, = 2 for latency, and 3 for Energy, and 4 for overhead


#Get Data from metrics files
t = 0
for num_mules in folder_nums:
    directory = "Bands_UMass" + num_mules + "/" + day + "/Day2/"

    for band in bands:
        directory_band = directory + band + "/"

        for protocol in protocols:

            directory_band_proto = directory_band + protocol + "/"

            if protocol == "XChants":
                metrics_file = "metrics_LLC_day2_X-CHANTS.txt"
            elif protocol == "Epidemic":
                metrics_file = "metrics_LLC_day2_Epi.txt"
            elif protocol == "SprayNWait":
                metrics_file = "metrics_LLC_day2_SnW.txt"
            elif protocol == "HotPotato":
                metrics_file = "metrics_LLC_day2_HP.txt"

            with open(directory_band_proto + metrics_file) as f:
                lines = f.readlines()[1:]

            for line in lines:
                line_arr = line.strip().split()

                if "180" in line_arr:

                    if "XChants" == routing_folder:
                        if "ALL" == band:
                            Xchants[t] = line_arr[p_id]

                    elif "Epidemic" == routing_folder:
                        if "ALL" == band:
                            Epidemic_ALL[t] = line_arr[p_id]
                        elif "LTE" == band:
                            Epidemic_LTE[t] = line_arr[p_id]
                        elif "TV" == band:
                            Epidemic_TV[t] = line_arr[p_id]
                        elif "CBRS" == band:
                            Epidemic_CBRS[t] = line_arr[p_id]
                        elif "ISM" == band:
                            Epidemic_ISM[t] = line_arr[p_id]

                    elif "SprayNWait" == routing_folder:
                        if "ALL" == band:
                            SprayNWait_ALL[t] = line_arr[p_id]

                    elif "HotPotato" == routing_folder:
                        if "ALL" == band:
                            HotPotato_ALL[t] = line_arr[p_id]
    t += 1

t = 0
for num_mules in folder_nums:
    metric_file = open("../Bands_UMass" + str(num_mules) +"/" + day + "/Day2/ALL/XChants/metrics_LLC_day2_X-CHANTS_opt.txt", "r")
    lines = metric_file.readlines()[1:]
    for line in lines:
        line_arr = line.strip().split("\t")

        if "180" in line_arr[0]:

            Xchants_pk[t] = line_arr[p_id]
    t += 1


#Create plot
x = np.array([2, 4, 6, 8, 10, 12])
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
plt.xticks(np.arange(2, 13, step=2))

fig_name = "dummy.eps"

if p_id == 1:
    plt.ylabel('Packet delivery ratio', fontsize=25)
    plt.xlabel('Number of Buses', fontsize=25)

    fig_name = "../Plots/pdr_nodes_UMass.eps"

if p_id == 2:
    plt.ylabel('Latency (min)', fontsize=25)
    plt.xlabel('Number of Buses', fontsize=25)

    fig_name = "../Plots/latency_nodes_UMass.eps"

if p_id == 3:
    plt.ylabel('Energy Expenditure (KJ)', fontsize=25)
    plt.xlabel('Number of Buses', fontsize=25)

    fig_name = "../Plots/energy_nodes_UMass.eps"

if p_id == 4:
    plt.ylabel('Message overhead', fontsize=25)
    plt.xlabel('Number of Buses', fontsize=25)

    fig_name = "../Plots/overhead_nodes_UMass.eps"

plt.errorbar(x, Xchants_pk, 0, marker='o', linestyle='-', linewidth=2)
plt.errorbar(x, Xchants, 0, marker='o', linestyle='-', linewidth=2)
plt.errorbar(x, Epidemic_ALL, 0, marker='*', linestyle='--', linewidth=2)
plt.errorbar(x, Epidemic_CBRS, 0, marker='*', linestyle=':', linewidth=2)
plt.errorbar(x, Epidemic_ISM, 0, marker='*', linestyle='--', linewidth=2)
plt.errorbar(x, Epidemic_LTE, 0, marker='*', linestyle='-.', linewidth=2)
plt.errorbar(x, Epidemic_TV, 0, marker='*', linestyle='-.', linewidth=2)
plt.errorbar(x, SprayNWait_ALL, 0, marker='D', linestyle='--', linewidth=2)
plt.errorbar(x, HotPotato_ALL, 0, marker='^', linestyle='--', linewidth=2)

plt.tight_layout()
plt.savefig(fig_name)

plt.show()


