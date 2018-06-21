from constants import *


def message_info(mes_list):
    with open(path_to_folder + delivery_file_name, 'r') as f:
        lines = f.readlines()

    file = open(path_to_folder + notDelivered_file_name, 'w')

    for id in mes_list:
        for line in lines:
            line_arr = line.strip().split()
            if int(id) == int(line_arr[0]):
                file.write(line)
    file.close()


def compute_metrics(lines, total_messages, delivery_time):
    delivered = 0
    latency = 0
    energy = 0
    mes_IDs = []
    #all_IDs = [x for x in range(num_messages)]
    unique_messages = []

    for line in lines:
        line_arr = line.strip().split("\t")
        if int(line_arr[4]) <= delivery_time and int(line_arr[0]) not in mes_IDs:
            delivered += 1
            latency += int(line_arr[5])
            # energy += float(line_arr[7])
            unique_messages.append(line_arr)
            mes_IDs.append(int(line_arr[0]))
            #all_IDs.remove(int(line_arr[0]))


    if delivered > 0:
        latency = float(latency)/delivered
        energy = float(energy)/delivered

    if total_messages > 0:
        delivered = float(delivered) / total_messages

    print("t: ", t, " msg: ", total_messages, " del: ", delivered, "lat: ", latency)

    return delivered, latency, energy, mes_IDs, unique_messages

#Main starts here
max_nodes = 23
msg_file = open("../Bands_UMass" + str(max_nodes) + "/" + Link_Exists_path.split("/")[2] + "/Day1/" + "generated_messages.txt", "r")
total_messages = len(msg_file.readlines()[1:])

metric_file = open(path_to_folder + metrics_file_name, "w")
f = open(path_to_folder + delivery_file_name, "r")

lines = f.readlines()[2:]

fsorted = open(path_to_folder + "sorted_SnW_delivery.txt", "w")
#sort the lines based on LLC i.e., column 5

fsorted.write("ID	s	d	ts	te	LLC	size	parent	parentTime	replica\n")

lines = sorted(lines, key=lambda line: int(line.split()[5]))

for line in lines:
    fsorted.write(line)
fsorted.close()

delivery_times = [i for i in range(0, T + 10, 15)]

metric_file.write("#t\tPDR\tLatency\tEnergy\n")
for t in delivery_times:
    avg_pdr, avg_latency, avg_energy, mes_IDs, unique_messages = compute_metrics(lines, total_messages, t)
    metric_file.write(str(t) + "\t" + str(avg_pdr) + "\t" + str(avg_latency) + "\t" + str(avg_energy) + "\n")

metric_file.close()
# print("Delivered messages", sorted(mes_IDs))

with open(path_to_folder + "unique_SnW_messages.txt", "w") as f:
    f.write("ID\ts\td\tts\tte\tLLC\tsize\n")
    f.write("------------------------------\n")

    for msg_line in unique_messages:
        for word in msg_line[:7]:
            f.write(str(word) + "\t")
        f.write("\n")

# message_info(all_IDs)

