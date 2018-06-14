import matplotlib.pyplot as plt

T = 120
choice = 1

metrics_file = "metrics_LLC_day"
metricsOptions = ["2_X-CHANTS.txt", "1_Epi.txt", "1_SnW.txt", "1_HP.txt"]
protocols = ["XChants/", "Epidemic/", "SprayNWait/", "HotPotato/" ]
routing_path = "Bands_UMass/2007-10-31_2007-11-01/ALL/"

time = [i for i in range(0,T+10, 15)]
delivered = []
latency = []

for i in range(len(metricsOptions)):

    delivered_temp = []
    latency_temp = []

    metrics_file_path = routing_path + protocols[i] + metrics_file + metricsOptions[i]

    with open(metrics_file_path, "r") as f:
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
    plt.xticks(time)
    plt.ylabel('Packet delivery ratio', fontsize=25)
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
    plt.ylabel('Latency', fontsize=25)
    for i in range(len(latency)):
        if i == 0:
            plt.plot(time, delivered[i], marker='o', linestyle='-', linewidth=2)
        elif i == 1:
            plt.plot(time, delivered[i], marker='*', linestyle='--', linewidth=2)
        elif i == 2:
            plt.plot(time, delivered[i], marker='^', linestyle=':', linewidth=2)
        elif i == 3:
            plt.plot(time, delivered[i], marker='D', linestyle='--', linewidth=2)

plt.legend([ 'XCHANTS', 'Epidemic', 'SnW','Hot Potato'], loc="upper left", fontsize=20)
plt.tight_layout()
plt.savefig(routing_path + "Plots/Routing_PDR.png", format="png")
plt.show()


