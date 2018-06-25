import matplotlib.pyplot as plt

T = 180
choice = 2

metrics_file = "metrics_LLC_day"
metricsOptions = ["2_X-CHANTS.txt", "2_Epi.txt", "2_SnW.txt", "2_HP.txt"]
protocols = ["XChants/", "Epidemic/", "SprayNWait/", "HotPotato/" ]
# routing_path = "Bands_UMass23/2007-11-06/Day2/ALL/"
routing_paths = ["Bands_UMass18/2007-10-23/", "Bands_UMass16/2007-10-24/", "Bands_UMass20/2007-10-31/", "Bands_UMass21/2007-11-01/", "Bands_UMass23/2007-11-06/", "Bands_UMass16/2007-11-07/"]

for routing_path in routing_paths:

    time = [i for i in range(0,T+10, 15)]
    delivered = []
    latency = []
    energy = []

    for i in range(len(metricsOptions)):

        delivered_temp = []
        latency_temp = []
        energy_temp = []

        metrics_file_path = routing_path + "Day2/ALL/" + protocols[i] + metrics_file + metricsOptions[i]


        with open(metrics_file_path, "r") as f:
            metrics_lines = f.readlines()[1:]

        for j in range(len(metrics_lines)):
            metrics_line_arr = metrics_lines[j].strip()
            metrics_line_arr = metrics_line_arr.split()

            delivered_temp.append(float(metrics_line_arr[1]))
            latency_temp.append(float(metrics_line_arr[2]))
            energy_temp.append(float(metrics_line_arr[3]))


        delivered.append(delivered_temp)
        latency.append(latency_temp)
        energy.append(energy_temp)


    plt.xlabel('Simulation time (in minutes)', fontsize=25)

    # Packet delivery
    if choice == 0:
        plt.ylim(0, 1)
        plt.xticks(time)
        plt.ylabel('Packet delivery ratio', fontsize=25)
        fig_name = "Plots/Routing_PDR_time_UMass.png"
        for i in range(len(delivered)):
            if i == 0:
                plt.plot(time, delivered[i], marker='o', linestyle='-', linewidth=2)
            elif i == 1:
                plt.plot(time, delivered[i], marker='*', linestyle='--', linewidth=2)
            elif i == 2:
                plt.plot(time, delivered[i],  marker='^', linestyle=':', linewidth=2)
            elif i == 3:
                plt.plot(time, delivered[i], marker='D', linestyle='--', linewidth=2)




                # Latency
    elif choice == 1:
        plt.xticks(time)
        plt.ylabel('Latency (in minutes)', fontsize=25)
        fig_name = "Plots/Routing_Latency_time_UMass.png"
        for i in range(len(latency)):
            if i == 0:
                plt.plot(time, latency[i], marker='o', linestyle='-', linewidth=2)
            elif i == 1:
                plt.plot(time, latency[i], marker='*', linestyle='--', linewidth=2)
            elif i == 2:
                plt.plot(time, latency[i], marker='^', linestyle=':', linewidth=2)
            elif i == 3:
                plt.plot(time, latency[i], marker='D', linestyle='--', linewidth=2)

    elif choice == 2:
        plt.xticks(time)
        plt.ylabel('Energy', fontsize=25)
        fig_name = "Plots/Routing_Energy_time_UMass.png"
        for i in range(len(latency)):
            if i == 0:
                plt.plot(time, energy[i], marker='o', linestyle='-', linewidth=2)
            elif i == 1:
                plt.plot(time, energy[i], marker='*', linestyle='--', linewidth=2)
            elif i == 2:
                plt.plot(time, energy[i], marker='^', linestyle=':', linewidth=2)
            elif i == 3:
                plt.plot(time, energy[i], marker='D', linestyle='--', linewidth=2)

    plt.legend([ 'XCHANTS', 'Epidemic', 'SnW', 'Hot Potato'], loc="upper left", fontsize=20)
    plt.tight_layout()
    plt.savefig(fig_name, format="png")
    plt.show()


