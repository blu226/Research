import numpy as np
from STB_help import *
import matplotlib.pyplot as plt
from constants import *


directory = "Bands/ALL/"
files = ["metrics_LLC_day1.txt", "metrics_LLC_day2.txt"]
time = [i for i in range(0, T + 10, 10)]
choice = 0

delivered = []
latency = []

if choice == 0:
    fig_name = "delivery_day1vday2.eps"
else:
    fig_name = "latency_day1vday2.eps"

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
            # print(time)
            # print(delivered[i])
            plt.plot(time, delivered[i])

    # Latency
    elif choice == 1:
        plt.ylabel('Latency', fontsize=25)
        for i in range(len(latency)):
            plt.plot(time, latency[i])

    plt.legend(['Day1', 'Day2'], loc="upper left", fontsize=20)
    plt.tight_layout()
    title = "UMass Simulation"
    plt.title(title)
    plt.show()
    plt.savefig(fig_name)



