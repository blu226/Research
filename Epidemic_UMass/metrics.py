from constants import *

def compute_overhead(time):
    path_to_mess_arr = Link_Exists_path.split('/')
    path_to_mess = path_to_mess_arr[0] + '/' + path_to_mess_arr[1] + '/' + path_to_mess_arr[2] + '/Day1/generated_messages.txt'

    with open(generated_messages_file, 'r') as f:
        generated_lines = f.readlines()[1:]

    with open(path_to_folder + delivery_file_name, 'r') as f:
        delivered_lines = f.readlines()[2:]

    with open(path_to_folder + notDelivered_file_name, 'r') as f:
        NotDelivered_lines = f.readlines()[2:]

    num_mes_gen = 0
    num_mes_del = 0
    num_mes_NotDel = 0

    for line in generated_lines:
        line_arr = line.strip().split()
        if int(line_arr[4]) <= time:
            num_mes_gen += 1

    for line in delivered_lines:
        line_arr = line.strip().split()
        if int(line_arr[4]) <= time:
            num_mes_del += 1

    for line in NotDelivered_lines:
        line_arr = line.strip().split()
        if int(line_arr[4]) <= time:
            num_mes_NotDel += 1

    if num_mes_gen == 0:
        return 0

    overhead = (num_mes_del + num_mes_NotDel) / num_mes_gen

    return overhead



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
    band_usage = [0,0,0,0]
    mes_IDs = []
    unique_messages = []

    overhead = compute_overhead(delivery_time)

    for line in lines:
        line_arr = line.strip().split()

        if int(line_arr[4]) <= delivery_time and int(line_arr[0]) not in mes_IDs:
            delivered += 1
            latency += int(line_arr[6])
            band_usage[0] += int(line_arr[10])
            band_usage[1] += int(line_arr[11])
            band_usage[2] += int(line_arr[12])
            band_usage[3] += int(line_arr[13])
            # energy += float(line_arr[7])
            unique_messages.append(line_arr)
            mes_IDs.append(int(line_arr[0]))

    total_links = sum(band_usage)
    if total_links == 0:
        total_links = 1

    if delivered > 0:
        latency = float(latency)/delivered
        energy = float(energy)/delivered

    if total_messages > 0:
        delivered = float(delivered) / total_messages

    print("t: ", t, " msg: ", total_messages, " del: ", delivered, "lat: ", latency, "overhead: ", overhead)
    print("band usage: TV = " + str(band_usage[0]/total_links) + " ISM = " + str(band_usage[1]/total_links) + " LTE = " + str(band_usage[2]/total_links) + " CBRS = " + str(band_usage[3]/total_links))

    return delivered, latency, energy, mes_IDs, unique_messages, overhead

#Main starts here
path_to_mess_arr = Link_Exists_path.split('/')
path_to_mess = path_to_mess_arr[0] + '/' + path_to_mess_arr[1] + '/' + path_to_mess_arr[2] + '/Day1/generated_messages.txt'

msg_file = open(generated_messages_file, "r")
total_messages = len(msg_file.readlines()[1:])

metric_file = open(path_to_folder + metrics_file_name, "w")
f = open(path_to_folder + delivery_file_name, "r")

lines = f.readlines()[2:]

fsorted = open(path_to_folder+ "sorted_Epidemic_delivery.txt", "w")
#sort the lines based on LLC i.e., column 5

fsorted.write("ID	s	d	ts	te	LLC	size	parent	parentTime	replica\n")

lines = sorted(lines, key=lambda line: int(line.split()[5]))

for line in lines:
    fsorted.write(line)
fsorted.close()

delivery_times = [i for i in range(0, T + 10, 15)]

metric_file.write("#t\tPDR\tLatency\tEnergy\n")
for t in delivery_times:
    avg_pdr, avg_latency, avg_energy, mes_IDs, unique_messages, overhead = compute_metrics(lines, total_messages, t)
    metric_file.write(str(t) + "\t" + str(avg_pdr) + "\t" + str(avg_latency) + "\t" + str(avg_energy) + "\t" + str(overhead) + "\n")

metric_file.close()
# print("Delivered messages", sorted(mes_IDs))

with open(path_to_folder + "unique_Epidemic_messages.txt", "w") as f:
    f.write("ID\ts\td\tts\tte\tLLC\tsize\n")
    f.write("------------------------------\n")

    for msg_line in unique_messages:
        for word in msg_line[:7]:
            f.write(str(word) + "\t")
        f.write("\n")

# message_info(all_IDs)

