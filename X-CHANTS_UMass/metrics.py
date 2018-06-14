from constants import *

def compute_overhead(time):

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
    mes_IDs = []
    unique_messages = []

    # overhead = compute_overhead(delivery_time)

    for line in lines:
        line_arr = line.strip().split("\t")
        if int(line_arr[4]) <= delivery_time and int(line_arr[0]) not in mes_IDs:
            delivered += 1
            latency += int(line_arr[5])
            # energy += float(line_arr[7])
            unique_messages.append(line_arr)
            mes_IDs.append(int(line_arr[0]))


    if delivered > 0:
        latency = float(latency)/delivered
        energy = float(energy)/delivered

    if total_messages > 0:
        delivered = float(delivered) / total_messages

    print("t: ", t, " msg: ", total_messages, " del: ", delivered, "lat: ", latency)

    return delivered, latency, energy, mes_IDs, unique_messages

#Main starts here
path_to_mess_arr = link_exists_folder.split('/')
path_to_mess = path_to_mess_arr[0] + '/' + path_to_mess_arr[1] + '/' + path_to_mess_arr[2] + '/Day1/generated_messages.txt'

msg_file = open(path_to_mess, "r")
total_messages = len(msg_file.readlines()[1:])

metric_file = open(path_to_folder + metrics_file_name, "w")
f = open(path_to_folder + delivery_file_name, "r")

lines = f.readlines()[2:]


delivery_times = [i for i in range(0, T + 10, 15)]

metric_file.write("#t\tPDR\tLatency\tEnergy\n")
for t in delivery_times:
    avg_pdr, avg_latency, avg_energy, mes_IDs, unique_messages = compute_metrics(lines, total_messages, t)
    metric_file.write(str(t) + "\t" + str(avg_pdr) + "\t" + str(avg_latency) + "\t" + str(avg_energy) +  "\n")

metric_file.close()
# print("Delivered messages", sorted(mes_IDs))



# message_info(all_IDs)

