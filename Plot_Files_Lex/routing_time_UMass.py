import matplotlib.pyplot as plt

T = 180
choice = 3

metrics_file = "metrics_LLC_day"
metricsOptions = ["2_X-CHANTS.txt", "2_Epi.txt", "2_SnW.txt", "2_SnW.txt", "2_HP.txt"]
protocols = ["XChants/", "Epidemic/", "SprayNWait/","SprayNWait5/",  "HotPotato/" ]
# routing_path = "Bands_UMass23/2007-11-06/Day2/ALL/"
routing_paths = ["../Bands_UMass23/2007-11-06/"]

for routing_path in routing_paths:

    time = [i for i in range(0,T+10, 30)]
    delivered = []
    latency = []
    energy = []
    overhead = []

    for i in range(len(metricsOptions)):

        delivered_temp = []
        latency_temp = []
        energy_temp = []
        overhead_temp = []

        metrics_file_path = routing_path + "Day2/ALL/" + protocols[i] + metrics_file + metricsOptions[i]


        with open(metrics_file_path, "r") as f:
            metrics_lines = f.readlines()[1:]

        for j in range(len(metrics_lines)):
            if j % 2 == 0:
                metrics_line_arr = metrics_lines[j].strip()
                metrics_line_arr = metrics_line_arr.split()

                delivered_temp.append(float(metrics_line_arr[1]))
                latency_temp.append(float(metrics_line_arr[2]))
                energy_temp.append(float(metrics_line_arr[3]))
                overhead_temp.append(float(metrics_line_arr[4]))
                if metricsOptions[i] == "2_HP.txt":
                    print("overhead: ", overhead_temp)

        delivered.append(delivered_temp)
        latency.append(latency_temp)
        energy.append(energy_temp)
        overhead.append(overhead_temp)


    plt.xlabel('Simulation time (min)', fontsize=25)

    # Packet delivery
    if choice == 0:
        plt.ylim(0, 1.1)
        plt.xticks(time)
        plt.ylabel('Message Delivery Ratio', fontsize=25)
        fig_name = "../Plots/Routing_PDR_time_UMass.eps"
        for i in range(len(delivered)):
            if i == 0:
                plt.plot(time, delivered[i], marker='o', linestyle='-', linewidth=2)
            elif i == 1:
                plt.plot(time, delivered[i], marker='*', linestyle='--', linewidth=2)
            elif i == 2:
                plt.plot(time, delivered[i],  marker='^', linestyle=':', linewidth=2)
            elif i == 3:
                plt.plot(time, delivered[i], marker='^', linestyle='--', linewidth=2)
            elif i == 4:
                plt.plot(time, delivered[i], marker='D', linestyle='--', linewidth=2)




                # Latency
    elif choice == 1:
        plt.xticks(time)
        plt.ylabel('Network Delay (min)', fontsize=25)
        fig_name = "../Plots/Routing_Latency_time_UMass.eps"
        for i in range(len(latency)):
            if i == 0:
                plt.plot(time, latency[i], marker='o', linestyle='-', linewidth=2)
            elif i == 1:
                plt.plot(time, latency[i], marker='*', linestyle='--', linewidth=2)
            elif i == 2:
                plt.plot(time, latency[i], marker='^', linestyle=':', linewidth=2)
            elif i == 3:
                plt.plot(time, latency[i], marker='^', linestyle='--', linewidth=2)
            elif i == 4:
                plt.plot(time, latency[i], marker='D', linestyle='--', linewidth=2)

    elif choice == 2:
        plt.xticks(time)
        plt.ylabel('Energy Expenditure', fontsize=25)
        fig_name = "../Plots/Routing_Energy_time_UMass.eps"
        for i in range(len(latency)):
            if i == 0:
                plt.plot(time, energy[i], marker='o', linestyle='-', linewidth=2)
            elif i == 1:
                plt.plot(time, energy[i], marker='*', linestyle='--', linewidth=2)
            elif i == 2:
                plt.plot(time, energy[i], marker='^', linestyle=':', linewidth=2)
            elif i == 3:
                plt.plot(time, energy[i], marker='^', linestyle='--', linewidth=2)
            elif i == 4:
                plt.plot(time, energy[i], marker='D', linestyle='--', linewidth=2)

    if choice == 3:
        plt.xticks(time)
        plt.ylabel('Overhead', fontsize=25)
        fig_name = "../Plots/Routing_Overhead_time_UMass.eps"
        for i in range(len(overhead)):
            if i == 0:
                plt.plot(time, overhead[i], marker='o', linestyle='-', linewidth=2)
            elif i == 1:
                plt.plot(time, overhead[i], marker='*', linestyle='--', linewidth=2)
            elif i == 2:
                plt.plot(time, overhead[i],  marker='^', linestyle=':', linewidth=2)
            elif i == 3:
                plt.plot(time, overhead[i], marker='^', linestyle='--', linewidth=2)
            elif i == 4:
                plt.plot(time, overhead[i], marker='D', linestyle='--', linewidth=2)

    plt.legend(["X-CHANTS", "S-ER", "S-SnW (30)", "S-SnW (5)", "S-HP"], loc="upper left", fontsize=20)
    plt.tight_layout()
    plt.savefig(fig_name)
    plt.show()


