import numpy as np
from map_plot import *
import matplotlib.pyplot as plt
from constants import *

for j in range(2):
    day = j + 1
    for i in range(2):
        choice = i
        if i == 0:
            fig_name = "delivery_day" + str(day) + ".eps"
        else:
            fig_name = "latency_day" + str(day) + ".eps"

        folders = ["ALL/", "ISM/", "LTE/", "TV/", "CBRS/"]
        bands = "Bands/"
        time = [i for i in range(0,T + 10,10)]

        delivered = []
        latency = []

        #Get data from metrics files
        for folder in folders:
            directory = bands + folder + metrics_file_name
            print(directory)
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
                # print(time)
                # print(delivered[i])
                plt.plot(time, delivered[i])

        #Latency
        elif choice == 1:
            plt.ylabel('Latency', fontsize=25)
            for i in range(5):
                plt.plot(time, latency[i])

        plt.legend(['X-CHANTS', 'ISM', 'LTE', 'TV', 'CBRS'], loc = "upper left", fontsize = 20)
        plt.tight_layout()
        title = "UMass Simulation Day " + str(day)
        plt.title(title)
        plt.show()
        plt.savefig(fig_name)

