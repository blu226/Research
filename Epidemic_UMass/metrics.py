from constants import *

def compute_overhead(time):
    max_nodes = V
    with open( "../Bands_UMass" + str(max_nodes) + "/" + Link_Exists_path.split("/")[2] + "/Day1/" + "generated_messages.txt", "r") as f:
        generated_lines = f.readlines()[1:]

    with open(path_to_folder + delivery_file_name, 'r') as f:
        delivered_lines = f.readlines()[2:]

    with open(path_to_folder + notDelivered_file_name, 'r') as f:
        NotDelivered_lines = f.readlines()[2:]

    num_mes_gen = 0
    num_mes_del = 0
    num_mes_NotDel = 0

    sum_mes_gen = 0
    sum_mes_del = 0
    sum_mes_NotDel = 0

    for line in generated_lines:
        line_arr = line.strip().split()
        if int(line_arr[5]) < time:
            num_mes_gen += 1
            sum_mes_gen += int(line_arr[4])
    for line in delivered_lines:
        line_arr = line.strip().split()
        if int(line_arr[4]) < time:
            num_mes_del += 1
            sum_mes_del += int(line_arr[6])

    for line in NotDelivered_lines:
        line_arr = line.strip().split()
        if int(line_arr[4]) < time:
            num_mes_NotDel += 1
            sum_mes_NotDel += int(line_arr[6])



    if num_mes_gen == 0 or num_mes_del + num_mes_NotDel == 0:
        return 0

    overhead = (num_mes_del + num_mes_NotDel) / num_mes_gen
    overhead_size = (sum_mes_gen + sum_mes_NotDel)/sum_mes_gen

    return overhead

def find_avg_energy(time):

    with open(path_to_folder + consumedEnergyFile, 'r') as f:
        lines = f.readlines()[1:]

    for line in lines:
        line_arr = line.strip().split()
        if (int(line_arr[0]) == int(time) or int(line_arr[0]) == T - 1):
            return line_arr[1]


def message_info(mes_list):
    with open(Link_Exists_path + generated_file_name, 'r') as f:
        lines = f.readlines()

    file = open("NOT_delivered.txt", 'w')

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
    band_usage = [0, 0, 0, 0]

    #all_IDs = [x for x in range(num_messages)]
    unique_messages = []

    for line in lines:
        line_arr = line.strip().split()
        if int(line_arr[4]) <= delivery_time and int(line_arr[0]) not in mes_IDs:
            delivered += 1
            latency += int(line_arr[5])
            # energy += float(line_arr[7])
            unique_messages.append(line_arr)
            mes_IDs.append(int(line_arr[0]))
            band_usage[0] += int(line_arr[10])
            band_usage[1] += int(line_arr[11])
            band_usage[2] += int(line_arr[12])
            band_usage[3] += int(line_arr[13])

        total = band_usage[0] + band_usage[1] + band_usage[2] + band_usage[3]
        if total > 0:
            band_usage = [ele/ total for ele in band_usage]

    if delivered > 0:
        latency = round(float(latency)/delivered, 2)
        energy = float(energy)/delivered

    if total_messages > 0:
        delivered = round(float(delivered) / total_messages, 2)

    avg_energy = find_avg_energy(delivery_time)

    overhead = round(compute_overhead(delivery_time), 2)

    print("t: ", t, " msg: ", total_messages, " del: ", delivered, "lat: ", latency, " Overhead: ", overhead, "Energy: ", avg_energy)

    return delivered, latency, avg_energy, mes_IDs, unique_messages, overhead, band_usage

#Main starts here
max_nodes = V
msg_file = open("../Bands_UMass" + str(max_nodes) + "/" + Link_Exists_path.split("/")[2] + "/Day1/" + "generated_messages.txt", "r")
total_messages = len(msg_file.readlines()[1:])

metric_file = open(path_to_folder + metrics_file_name, "w")
f = open(path_to_folder + delivery_file_name, "r")

lines = f.readlines()[2:]

fsorted = open(path_to_folder + "sorted_epidemic_delivery.txt", "w")
#sort the lines based on LLC i.e., column 5

fsorted.write("ID	s	d	ts	te	LLC	size	parent	parentTime	replica\n")

lines = sorted(lines, key=lambda line: int(line.split()[5]))

for line in lines:
    fsorted.write(line)
fsorted.close()

delivery_times = [i for i in range(0, T + 10, 15)]

metric_file.write("#t\tPDR\tLatency\tEnergy\Overhead\n")
for t in delivery_times:
    avg_pdr, avg_latency, avg_energy, mes_IDs, unique_messages, overhead, band_usage = compute_metrics(lines, total_messages, t)
    metric_file.write(
        str(t) + "\t" + str(avg_pdr) + "\t" + str(avg_latency) + "\t" + str(avg_energy) + "\t" + str(overhead) + "\t" +
        str(band_usage[0]) + "\t" + str(band_usage[1]) + "\t" + str(band_usage[2]) + "\t" + str(band_usage[3]) + "\n")

metric_file.close()
# print("Delivered messages", sorted(mes_IDs))

with open(path_to_folder + "unique_epidemic_messages.txt", "w") as f:
    f.write("ID\ts\td\tts\tte\tLLC\tsize\n")
    f.write("------------------------------\n")

    for msg_line in unique_messages:
        for word in msg_line[:7]:
            f.write(str(word) + "\t")
        f.write("\n")

# message_info(all_IDs)

