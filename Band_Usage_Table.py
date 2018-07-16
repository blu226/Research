with open("Plots/Band_Usage.txt", 'w') as f:
    f.write("Protocol\tTV\tLTE\tISM\tCBRS\tTemporal\n")

metrics_file = "metrics_LLC_day"
metricsOptions = ["2_X-CHANTS.txt", "2_Epi.txt", "2_SnW.txt", "2_HP.txt"]
protocols = ["XChants/", "Epidemic/", "SprayNWait/", "HotPotato/" ]
routing_path = "Bands_UMass23/2007-11-06/Day2/ALL/"

file = open("Plots/Band_Usage.txt", 'a')

for i in range(len(metricsOptions)):

    metrics_file_path = routing_path + protocols[i] + metrics_file + metricsOptions[i]

    with open(metrics_file_path, "r") as f:
        metrics_lines = f.readlines()[1:]

    last_line = len(metrics_lines) - 1

    metrics_line_arr = metrics_lines[last_line].strip()
    metrics_line_arr = metrics_line_arr.split()


    tv = float(metrics_line_arr[5]) * 100
    ism = float(metrics_line_arr[6]) * 100
    lte = float(metrics_line_arr[7]) * 100
    cbrs = float(metrics_line_arr[8]) * 100

    if i == 0:
        temporal = float(metrics_line_arr[9][:5]) * 100
    else:
        temporal = 0

    print(protocols[i] + "\t" + str(tv) + "\t" + str(lte) + "\t" + str(ism) + "\t" + str(cbrs) + "\t" + str(temporal) + "\n")
    file.write(protocols[i] + "\t" + str(tv) + "\t" + str(lte) + "\t" + str(ism) + "\t" + str(cbrs) + "\t" + str(temporal) + "\n")

file.close()
