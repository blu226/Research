import numpy as np
from map_plot import *
import matplotlib.pyplot as plt

choice = 0
fig_name = "delivery.eps"

folders = ["ALL/", "ISM/", "LTE/", "TV/", "CBRS/"]
bands = "Bands/"
time = [10, 20, 30, 40, 50, 60, 70, 80, 90]
delivered = []
latency = []

#Get data from metrics files
for folder in folders:
    directory = bands + folder + "metrics_LLC_day1.txt"

    delivered_temp = []
    latency_temp = []

    with open(directory, "r") as f:
        metrics_lines = f.readlines()[1:]

    for i in range(len(metrics_lines)):
        metrics_line_arr = metrics_lines[i].strip()
        metrics_line_arr = metrics_line_arr.split()

        delivered_temp.append(metrics_line_arr[1])
        latency_temp.append(metrics_line_arr[2])

    delivered.append(delivered_temp)
    latency.append(latency_temp)

#plot data
plt.xlabel('Simulation time', fontsize=25)
#Packet delivery
if choice == 0:
    plt.ylim(0, 1)
    plt.ylabel('Packet delivery ratio',  fontsize=25)
    for i in range(5):
        plt.plot(time, delivered[i])

#Latency
elif choice == 1:
    plt.ylabel('Latency', fontsize=25)
    for i in range(5):
        plt.plot(time, latency[i])

plt.legend(['X-CHANTS', 'LTE', 'TV', 'ISM', 'CBRS'], loc = "upper left", fontsize = 20)
plt.tight_layout()
#plt.show()
plt.savefig(fig_name)

