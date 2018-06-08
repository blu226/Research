import numpy as np
from STB_help import *
import matplotlib.pyplot as plt
from constants import *

def spectrumGraph(num, graph_title, dir):

    metrics_file = "metrics_LLC_day1_" + str(num) + "_180.txt"

    choice = 1
    if choice == 0:
        fig_name = dir + dir[5:] + "_DATA/deliveryDay1_" + graph_title + ".png"
    else:
        fig_name = dir + dir[5:] + "_DATA/latencyDay1_" + graph_title + ".png"

    folders = ["ALL/", "ISM/", "LTE/", "TV/", "CBRS/"]
    bands = dir + "/"
    time = [i for i in range(0,T + 10,10)]

    delivered = []
    latency = []
    energy = []

    #Get data from metrics files
    for folder in folders:
        directory = bands + folder + metrics_file
        delivered_temp = []
        latency_temp = []
        energy_temp = []

        with open(directory, "r") as f:
            metrics_lines = f.readlines()[1:]

        for i in range(len(metrics_lines)):
            metrics_line_arr = metrics_lines[i].strip()
            metrics_line_arr = metrics_line_arr.split()

            delivered_temp.append(metrics_line_arr[1])
            latency_temp.append(metrics_line_arr[2])
            energy_temp.append(metrics_line_arr[3])

        delivered.append(delivered_temp)
        latency.append(latency_temp)
        energy.append(energy_temp)

    #plot data
    plt.xlabel('Simulation time', fontsize=25)
    #Packet delivery
    if choice == 0:
        plt.ylim(0, 1)
        plt.ylabel('Packet delivery ratio',  fontsize=25)
        for i in range(5):
            # print(time)
            # print(delivered[i])
            plt.plot(time, delivered[i])

    #Latency
    elif choice == 1:
        plt.ylabel('Latency', fontsize=25)
        for i in range(5):
            plt.plot(time, latency[i])

    elif choice == 2:
        plt.ylabel('Energy', fontsize=25)
        for i in range(5):
            plt.plot(time, energy[i])

    plt.legend(['X-CHANTS', 'ISM', 'LTE', 'TV', 'CBRS'], loc = "upper left", fontsize = 20)
    plt.tight_layout()
    title = graph_title
    plt.title(title)
    plt.savefig(fig_name)
    plt.show()


directory = "Bands/"
folders = os.listdir(directory)
folders.sort()

for i in range(len(folders)):
    dir = directory + folders[i]
    dir_day = "DataMules/" + folders[i] + "/Day1/"
    num_buses = len(os.listdir(dir_day))
    spectrumGraph(num_buses,folders[i],dir)
