

metrics_file = "metrics_LLC_day"
metricsOptions = ["2_X-CHANTS.txt", "2_Epi.txt"]
protocols = ["XChants/", "Epidemic/" ]
routing_path = "Bands_UMass20/2007-11-06_2007-11-07/Day2/ALL/"

for i in range(len(metricsOptions)):

    metrics_file_path = routing_path + protocols[i] + metrics_file + metricsOptions[i]

    with open(metrics_file_path, "r") as f:
        metrics_lines = f.readlines()[1:]

    for j in range(len(metrics_lines)):
        metrics_line_arr = metrics_lines[j].strip()
        metrics_line_arr = metrics_line_arr.split()

        print