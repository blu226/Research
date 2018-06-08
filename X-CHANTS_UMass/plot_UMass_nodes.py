import numpy as np
from STB_help import *
import matplotlib.pyplot as plt
from constants import *

def get_data_array(data):
    new_data = []

    for i in range(len(data)):
        length = len(data[i]) -1
        new_data.append(data[i][length])
    print(new_data)
    return new_data

def get_metrics(day):
    delivered = []
    latency = []
    energy = []
    choice = 0
    num_nodes = [11,12,13,14,15,16]
    for num in num_nodes:
        metrics_file = "metrics_LLC_day" + str(day+1) + "_" + str(num) + "_120.txt"

        if choice == 0:
            fig_name = "delivery_" + metrics_file + ".eps"
        else:
            fig_name = "latency_day" + metrics_file + ".eps"

        folders = ["ALL/"]
        bands = "Bands/"




            #Get data from metrics files
        for folder in folders:
            directory = bands + folder + metrics_file
            print(directory)
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

    return delivered, latency, energy

        #plot data
plt.xlabel('Simulation time', fontsize=25)
#Packet delivery


num_nodes = [2,3,4,5,6,7]


for i in range(2):
    choice = i

    for j in range(2):
        delivered, latency, energy = get_metrics(j)


        if choice == 0:
            plt.ylim(0, 1)
            plt.ylabel('Packet delivery ratio',  fontsize=25)
            data = get_data_array((delivered))
            #for i in range(5):
                # print(time)
                # print(delivered[i])

            plt.plot(num_nodes, data)

        #Latency
        elif choice == 1:
            plt.ylabel('Latency', fontsize=25)
            data = get_data_array(latency)
            #for i in range(5):
            plt.plot(num_nodes, data)

        elif choice == 2:
            plt.ylabel('Energy', fontsize=25)
            data = get_data_array(energy)
            #for i in range(5):
            plt.plot(num_nodes, data)

    plt.legend(['Day 1', 'Day 2'], loc = "upper left", fontsize = 20)
    plt.tight_layout()
    title = "UMass Simulation Day 1 "
    plt.title(title)
    plt.show()
    #plt.savefig(fig_name)

