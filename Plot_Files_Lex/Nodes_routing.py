import numpy as np
import os
import matplotlib.pyplot as plt

time_epochs = 6
runs = 1
# 4 time stamps (15,30,45,60) and 10 runs
Xchants = np.zeros(shape=(time_epochs,runs))
Epidemic = np.zeros(shape=(time_epochs,runs))
SnW5 = np.zeros(shape=(time_epochs,runs))
SnW25 = np.zeros(shape=(time_epochs,runs))
SnW40 = np.zeros(shape=(time_epochs,runs))
HotPotato = np.zeros(shape=(time_epochs,runs))

folder_names = ["../Bands5/", "../Bands10/", "../Bands15/", "../Bands20/", "../Bands25/", "../Bands30/"]
#band_folders = ["XChants", "Epidemic", "SnW5", "SnW15", "HotPotato"]

p_id = 1  # p_id = 1 for PDR, = 2 for latency, and 3 for Energy

t = 0
for folder_name in folder_names:
    folders = os.listdir(folder_name)
    folders.sort()

    print("Folders: ", folders)

    #Run - 1, 2, 3
    for run in range(runs):
        print("============= Current folder ", folders[run])
        routing_folders = os.listdir(folder_name + folders[run] + "/" + "Day2/ALL/")

        for routing_folder in routing_folders:
            print("Routing folder: ", routing_folder)

            lines = []
            metric_file = ""

            if "XChants" == str(routing_folder):
                metric_file = open(folder_name + folders[
                    run] + "/" + "Day2/ALL" + "/" + routing_folder + "/" + "metrics_LLC_day2.txt")

            if "Epidemic" == str(routing_folder):
                metric_file = open(folder_name + folders[
                    run] + "/" + "Day2/ALL" + "/" + routing_folder + "/" + "metrics_epidemic_day2.txt")

            if "SnW25" == str(routing_folder):
                metric_file = open(folder_name + folders[
                    run] + "/" + "Day2/ALL" + "/" + routing_folder + "/" + "metrics_SnW_day2.txt")

            if "SnW25" == str(routing_folder):
                metric_file = open(folder_name + folders[
                    run] + "/" + "Day2/ALL" + "/" + routing_folder + "/" + "metrics_SnW_day2.txt")

            if "SnW25" == str(routing_folder):
                metric_file = open(folder_name + folders[
                    run] + "/" + "Day2/ALL" + "/" + routing_folder + "/" + "metrics_SnW_day2.txt")

            if "HotPotato" == str(routing_folder):
                metric_file = open(folder_name + folders[
                    run] + "/" + "Day2/ALL" + "/" + routing_folder + "/" + "metrics_hotPotato_day2.txt")

            if metric_file != "":
                lines = metric_file.readlines()[1:]

            # print(str(routing_folder), lines)

            for line in lines:
                line_arr = line.strip().split("\t")
                if "120" in line_arr[0]:
                    if "XChants" == str(routing_folder):
                        Xchants[t][run] = line_arr[p_id]
                    if "Epidemic" == str(routing_folder):
                        Epidemic[t][run] = line_arr[p_id]
                    if "SnW5" == str(routing_folder):
                        SnW5[t][run] = line_arr[p_id]
                    if "SnW25" == str(routing_folder):
                        SnW25[t][run] = line_arr[p_id]
                    if "SnW50" == str(routing_folder):
                        SnW40[t][run] = line_arr[p_id]
                    if "HotPotato" == str(routing_folder):
                        HotPotato[t][run] = line_arr[p_id]
                # print ("Here ", t, Epidemic[t][run])
    t = t + 1

Xchants_mean = []
Xchants_SD = []
Epidemic_mean = []
Epidemic_SD = []
SnW5_mean = []
SnW5_SD = []
SnW25_mean = []
SnW25_SD = []
SnW40_mean = []
SnW40_SD = []
HotPotato_mean = []
HotPotato_SD = []

print("XChants ", Xchants)
print("Epidemic ", Epidemic)

for i in range(len(Xchants)):

    Xchants_mean.append(np.mean(Xchants[i]))
    Xchants_SD.append(np.std(Xchants[i]))
    Epidemic_mean.append(np.mean(Epidemic[i]))
    Epidemic_SD.append(np.std(Epidemic[i]))
    SnW5_mean.append(np.mean(SnW5[i]))
    SnW5_SD.append(np.std(SnW5[i]))
    SnW25_mean.append(np.mean(SnW25[i]))
    SnW25_SD.append(np.std(SnW25[i]))
    SnW40_mean.append(np.mean(SnW40[i]))
    SnW40_SD.append(np.std(SnW40[i]))
    HotPotato_mean.append(np.mean(HotPotato[i]))
    HotPotato_SD.append(np.std(HotPotato[i]))

x = np.array([5, 10, 15, 20, 25, 30])
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)

fig_name = "dummy.eps"
if p_id == 1:
    plt.ylabel('Message Delivery Ratio', fontsize=25)
    plt.xlabel('Number of Datamules', fontsize=25)
    plt.yticks(fontsize=25)
    plt.ylim(0,1.1)
    fig_name = "../Plots/pdr_routing_nodes_day2.eps"


if p_id == 2:
    plt.ylabel('Network Delay (min)', fontsize=25)
    plt.xlabel('Number of Datamules', fontsize=25)
    plt.ylim(0,35)
    fig_name = "../Plots/latency_routing_nodes_day2.eps"

if p_id == 3:
    plt.ylabel('Energy Expenditure (J)', fontsize=25)
    plt.xlabel('Number of Datamules', fontsize=25)
    fig_name = "../Plots/energy_routing_nodes_day2.eps"


if p_id == 4:
    plt.ylabel('Message Overhead', fontsize=25)
    plt.ylim(10,65)
    plt.xlabel('Number of Datamules', fontsize=25)
    plt.ylim(0,65)
    fig_name = "../Plots/overhead_routing_nodes_day2.eps"


# plt.errorbar(x, Xchants_mean, Xchants_SD, marker='o', linestyle='-', linewidth=2)
plt.errorbar(x, Epidemic_mean, Epidemic_SD, marker='*', linestyle='--', linewidth=2)
# plt.errorbar(x, SnW5_mean, SnW5_SD, marker='^', linestyle=':', linewidth=2)
plt.errorbar(x, SnW25_mean, SnW25_SD, marker='^', linestyle=':', linewidth=2)
#plt.errorbar(x, SnW40_mean, SnW40_SD, marker='^', linestyle=':', linewidth=2)
plt.errorbar(x, HotPotato_mean, HotPotato_SD, marker='D', linestyle='--', linewidth=2)


if p_id == 1:
    plt.legend(["Epidemic", "SnW", "Hot Potato"], loc="upper left", fontsize=20, ncol = 2)

if p_id == 2:
    plt.legend(["Epidemic", "SnW", "Hot Potato"], loc="upper center", fontsize=20, ncol = 2)

if p_id == 3:
    plt.legend(["Epidemic", "SnW", "Hot Potato"], loc="upper right", fontsize=20)

if p_id == 4:
    plt.legend(["Epidemic", "SnW", "Hot Potato"], loc="center", fontsize=20, ncol = 2)

plt.tight_layout()
plt.savefig(fig_name)

plt.show()
