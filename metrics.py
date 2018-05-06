from constants import *

def compute_metrics(lines, total_messages, delivery_time):
    delivered = 0
    latency = 0
    energy = 0

    for line in lines:
        line_arr = line.strip().split("\t")
        if int(line_arr[4]) < delivery_time:
            delivered += 1
            latency += int(line_arr[6])
            energy += float(line_arr[7])

    if delivered > 0:
        latency = float(latency)/delivered
        energy = float(energy)/delivered

    if total_messages > 0:
        delivered = float(delivered) / total_messages

    print("t: ", t, " msg: ", total_messages, " del: ", delivered, "lat: ", latency)

    return delivered, latency, energy


#Main starts here
msg_file = open ("Bands"+ str(max_nodes) + "/" + link_exists_folder.split("/")[1] + "/" + "generated_messages.txt")
total_messages = len(msg_file.readlines()[1:])

metric_file = open(path_to_folder + metrics_file_name, "w")
f = open(path_to_folder + delivery_file_name, "r")

lines = f.readlines()[2:]

delivery_times = [5, 10, 20, 30, 40, 50, 60]


metric_file.write("#t\tPDR\tLatency\tEnergy\n")
for t in delivery_times:
    avg_pdr, avg_latency, avg_energy = compute_metrics(lines, total_messages, t)
    metric_file.write(str(t) + "\t" + str(avg_pdr) + "\t" + str(avg_latency) + "\t" + str(avg_energy) + "\n")

metric_file.close()