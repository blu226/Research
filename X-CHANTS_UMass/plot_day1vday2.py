import numpy as np
from STB_help import *
import matplotlib.pyplot as plt
from constants import *

def day1vsday2graph(graph_choice, directory, files, graph_title):
    time = [i for i in range(0,T+10, 10)]
    choice = graph_choice

    delivered = []
    latency = []

    if choice == 0:
        fig_name = directory + "/ALL/X-Chants/" + graph_title + "_PDR.png"
    else:
        fig_name = directory + "/ALL/X-Chants/" + graph_title + "_LLC.png"

    for file in files:
        path = directory + file


        delivered_temp = []
        latency_temp = []

        with open(path, "r") as f:
            metrics_lines = f.readlines()[1:]

        for i in range(len(metrics_lines)):
            metrics_line_arr = metrics_lines[i].strip()
            metrics_line_arr = metrics_line_arr.split()

            delivered_temp.append(metrics_line_arr[1])
            latency_temp.append(metrics_line_arr[2])

        delivered.append(delivered_temp)
        latency.append(latency_temp)

        plt.xlabel('Simulation time', fontsize=25)
        # Packet delivery
        if choice == 0:
            plt.ylim(0, 1)
            plt.ylabel('Packet delivery ratio', fontsize=25)
            for i in range(len(delivered)):
                plt.plot(time, delivered[i])

        # Latency
        elif choice == 1:
            plt.ylabel('Latency', fontsize=25)
            for i in range(len(latency)):
                plt.plot(time, latency[i])

        plt.legend(['Day1', 'Day2'], loc="upper left", fontsize=20)
        plt.tight_layout()
        title = graph_title
        plt.title(title)
        plt.savefig(fig_name, format="png")
        plt.show()

directory = "../Bands_UMass/"
folders = os.listdir(directory)
folders.sort()

# for i in range(len(folders)):
for j in range(2):
    dir = directory + "2007-10-31_2007-11-01"
    dir_day = "../DataMules/2007-10-31_2007-11-01/Day1/"
    num_buses = len(os.listdir(dir_day))
    file1 = "/ALL/X-Chants/metrics_LLC_day1_X-CHANTS.txt"
    file2 = "/ALL/X-Chants/metrics_LLC_day2_X-CHANTS.txt"
    files = [file1, file2]
    day1vsday2graph(j, dir, files, "X-CHANTS_Day1vDay2")


