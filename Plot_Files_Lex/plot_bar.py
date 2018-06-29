import numpy as np
import matplotlib.pyplot as plt

p_id = 1  # p_id = 1 for PDR, = 2 for latency, and 3 for Energy

folder_name = "../Bands30/1"
routing_folders = ["Epidemic", "SnW25", "HotPotato"]
bands = ["ALL/", "TV/", "LTE/", "ISM/", "CBRS/"]

ALL = []
TV = []
LTE = []
ISM = []
CBRS = []


for routing_folder in routing_folders:

    for band in bands:

        lines = []
        metric_file = ""

        if "XChants" == str(routing_folder):
            metric_file = open(folder_name + "/Day2/" + band  + routing_folder + "/" + "metrics_LLC_day2.txt")

        if "Epidemic" == str(routing_folder):
            metric_file = open(folder_name  + "/Day2/" + band + routing_folder + "/" + "metrics_epidemic_day2.txt")

        if "SnW25" == str(routing_folder):
            metric_file = open(folder_name +  "/Day2/" + band + routing_folder + "/" + "metrics_SnW_day2.txt")

        if "SnW25" == str(routing_folder):
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
                        ALL.append(float(line_arr[p_id]))
                    if "TV/" == str(band):
                        TV.append(float(line_arr[p_id]))
                    if "LTE/" == str(band):
                        LTE.append(float(line_arr[p_id]))
                    if "ISM/" == str(band):
                        ISM.append(float(line_arr[p_id]))
                    if "CBRS/" == str(band):
                        CBRS.append(float(line_arr[p_id]))


fig, ax = plt.subplots()
index = np.arange(num_protocols)

bar_width = 0.15
opacity = 0.4
label_offset = .225
num_protocols = len(routing_folders)

rects1 = ax.bar(index, ALL, bar_width, alpha = opacity, color = 'r', label = 'ALL')
rects2 = ax.bar(index + (1*bar_width), TV, bar_width, alpha = opacity, color = 'b', label = 'TV')
rects3 = ax.bar(index + (2*bar_width), LTE, bar_width, alpha = opacity, color = 'g', label = 'LTE')
rects4 = ax.bar(index + (3*bar_width), ISM, bar_width, alpha = opacity, color = 'y', label = 'ISM')
rects5 = ax.bar(index + (4*bar_width), CBRS, bar_width, alpha = opacity, color = '#FF00FF', label = 'CBRS')



if p_id == 1:
    ax.set_ylabel('Message Delivery Ratio')
    fig_name = "../Plots/PDR_bar.eps"
elif p_id == 2:
    ax.set_ylabel('Network Delay (min)')
    fig_name = "../Plots/Latency_bar.eps"
elif p_id == 3:
    ax.set_ylabel('Energy Expenditure (J)')
    fig_name = "../Plots/Energy_bar.eps"

ax.set_xlabel('Routing Protocols')
ax.set_xticks(index + bar_width + label_offset)
ax.set_xticklabels(routing_folders)
ax.legend()

fig.tight_layout()
plt.savefig(fig_name)
plt.show()


