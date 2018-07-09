import numpy as np
import matplotlib.pyplot as plt
import os

p_id = 4  # p_id = 1 for PDR, = 2 for latency, and 3 for Energy

folder_name = "../Bands30/1"
routing_folders = ["Epidemic", "SnW25"]
bands = ["ALL/", "TV/", "LTE/", "ISM/", "CBRS/"]

ALL = []
TV = []
LTE = []
ISM = []
CBRS = []

if not os.path.exists("../Plots"):
    os.makedirs("../Plots")

for routing_folder in routing_folders:

    for band in bands:

        lines = []
        metric_file = ""

        if "XChants" == str(routing_folder):
            metric_file = open(folder_name + "/Day2/" + band  + routing_folder + "/" + "metrics_LLC_day2.txt")

        if "Epidemic" == str(routing_folder):
            metric_file = open(folder_name  + "/Day2/" + band + routing_folder + "/" + "metrics_epidemic_day2.txt")

        if "SnW15" == str(routing_folder):
            metric_file = open(folder_name +  "/Day2/" + band + routing_folder + "/" + "metrics_SnW_day2.txt")

        if "SnW45" == str(routing_folder):
            metric_file = open(folder_name +  "/Day2/" + band  + routing_folder + "/" + "metrics_SnW_day2.txt")

        if "SnW25" == str(routing_folder):
            metric_file = open(folder_name + "/Day2/" + band  + routing_folder + "/" + "metrics_SnW_day2.txt")

        if "HotPotato" == str(routing_folder):
            metric_file = open(folder_name + "/Day2/" + band  + routing_folder + "/" + "metrics_hotPotato_day2.txt")

        if metric_file != "":
            lines = metric_file.readlines()[1:]

            for line in lines:
                line_arr = line.strip().split("\t")
                if "120" in line_arr[0]:

                    if "ALL/" == str(band):
                        if p_id == 3:
                            ALL.append(float(line_arr[p_id])/1000)
                        else:
                            ALL.append(float(line_arr[p_id]))
                    if "TV/" == str(band):
                        if p_id == 3:
                            TV.append(float(line_arr[p_id])/1000)
                        else:
                            TV.append(float(line_arr[p_id]))
                    if "LTE/" == str(band):
                        if p_id == 3:
                            LTE.append(float(line_arr[p_id])/1000)
                        else:
                            LTE.append(float(line_arr[p_id]))
                    if "ISM/" == str(band):
                        if p_id == 3:
                            ISM.append(float(line_arr[p_id])/1000)
                        else:
                            ISM.append(float(line_arr[p_id]))
                    if "CBRS/" == str(band):
                        if p_id == 3:
                            CBRS.append(float(line_arr[p_id])/1000)
                        else:
                            CBRS.append(float(line_arr[p_id]))



bar_width = 0.15
opacity = 0.5
label_offset = .225
num_protocols = len(routing_folders)

fig, ax = plt.subplots()
index = np.arange(num_protocols)

rects1 = ax.bar(index, ALL, bar_width, alpha = opacity, color = 'r', label = 'ALL', hatch="//")
rects2 = ax.bar(index + (1*bar_width), TV, bar_width, alpha = opacity, color = 'b', label = 'TV', hatch="*")
rects3 = ax.bar(index + (2*bar_width), LTE, bar_width, alpha = opacity, color = 'g', label = 'LTE', hatch='///')
rects4 = ax.bar(index + (3*bar_width), ISM, bar_width, alpha = opacity, color = 'y', label = 'ISM', hatch='**')
rects5 = ax.bar(index + (4*bar_width), CBRS, bar_width, alpha = opacity, color = '#FF00FF', label = 'CBRS', hatch='.')



if p_id == 1:
    ax.xaxis.set_tick_params(labelsize=20)
    ax.yaxis.set_tick_params(labelsize=20)
    ax.set_ylabel('Message Delivery Ratio', fontsize = "20")
    ax.set_xlabel(["ER", "SnW (15)", "SnW (25)"], fontsize = "20")
    fig_name = "../Plots/PDR_bar.eps"
elif p_id == 2:
    ax.set_ylim(0, 65)
    ax.xaxis.set_tick_params(labelsize=20)
    ax.yaxis.set_tick_params(labelsize=20)
    ax.set_ylabel('Network Delay (min)', fontsize = "20")
    ax.set_xlabel(["ER", "SnW (15)", "SnW (25)"], fontsize="20")
    fig_name = "../Plots/Latency_bar.eps"

elif p_id == 3:
    ax.xaxis.set_tick_params(labelsize=20)
    ax.yaxis.set_tick_params(labelsize=20)
    ax.set_ylabel('Energy Expenditure (KJ)', fontsize = "20")
    ax.set_xlabel(["ER", "SnW (15)", "SnW (25)"], fontsize="20")
    fig_name = "../Plots/Energy_bar.eps"

elif p_id == 4:
    ax.xaxis.set_tick_params(labelsize=20)
    ax.yaxis.set_tick_params(labelsize=20)
    ax.set_ylabel('Message Overhead', fontsize = "20")
    ax.set_xlabel(["ER", "SnW (15)", "SnW (25)"], fontsize="20")
    fig_name = "../Plots/Overhead_bar.eps"


ax.set_xlabel('Routing Protocols')
ax.set_xticks(index + bar_width + label_offset)
ax.set_xticklabels(routing_folders)
ax.legend()

fig.tight_layout()
plt.savefig(fig_name)
plt.show()


