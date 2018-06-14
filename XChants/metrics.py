from constants import *
import os

def compute_band_usage(lines, delivery_time, spec_lines):
    band_usage = [0, 0, 0, 0, 0]
    for sLine in spec_lines:
        sLine = sLine.strip().split()
        sLine = [int(obj) for obj in sLine]

        if sLine[2] + sLine[4] <= delivery_time:
            bands_arr = sLine[5:]
            # print(bands_arr)
            for band in bands_arr:
                if int(band) < 5:
                    band_usage[int(band) - 1] += 1
                else:
                    band_usage[4] += int(int(band)/10)
                    band_usage[int(band)%10] += 1


    total = sum(band_usage)
    if total > 0:
        band_usage = [(ele*100)/total for ele in band_usage]

    print("Del time ", delivery_time, "Band usage: ",  band_usage, "\n")
    return band_usage

def compute_metrics(lines, total_messages, delivery_time):
    delivered = 0
    latency = 0
    energy = 0
    overhead = 0

    for line in lines:
        line_arr = line.strip().split("\t")
        if int(line_arr[4]) <= delivery_time:
            delivered += 1
            latency += int(line_arr[6])
            energy += float(line_arr[7])

    if delivered > 0:
        latency = float(latency)/delivered
        energy = float(energy)/delivered

    if total_messages > 0:
        delivered = float(delivered) / total_messages

    if delivered > 0:
        overhead = 1

    print("t: ", t, " msg: ", total_messages, " del: ", delivered, "lat: ", latency, " Overhead: " , overhead)

    return delivered, latency, energy, overhead


#Main starts here

path_to_LLC_arr = path_to_folder.split('/')
path_to_Day1_LLC = path_to_LLC_arr[0] + "/" + path_to_LLC_arr[1] + '/' + path_to_LLC_arr[2] + '/Day1/' + path_to_LLC_arr[4] + '/' + path_to_LLC_arr[5] + '/' + path_to_LLC_arr[6] + '/'

print("Current file ", path_to_Day1_LLC)

msg_file = open ("../Bands"+ str(max_nodes) + "/" + link_exists_folder.split("/")[2] + "/Day1/generated_messages.txt")
total_messages = len(msg_file.readlines()[1:])

metric_file = open(path_to_folder + metrics_file_name, "w")
f = open(path_to_folder + delivery_file_name, "r")

lines = f.readlines()[2:]

with open(path_to_Day1_LLC + "LLC_Spectrum.txt", "r") as f:
    spec_lines = f.readlines()[1:]

# with open(path_to_Day1_LLC + "delivered_messages_spectrum.txt", "w") as f:
#     for sLine in spec_lines:
#         sLine_arr = sLine.strip().split()
#         sLine_arr = [int(obj) for obj in sLine_arr]
#
#         for line in lines:
#             line = line.strip().split()
#             line = [int(obj) for obj in line]
#
#             if sLine_arr[0] == line[1] and sLine_arr[1] == line[2] and sLine_arr[2] == line[3] and sLine_arr[2] + sLine_arr[4] <= T and sLine_arr[3] == line[5]:
#                 f.write(sLine)
#                 break

with open(path_to_Day1_LLC + "delivered_messages_spectrum.txt", "r") as f:
    del_spec_lines = f.readlines()

delivery_times = [i for i in range(0, T + 10, 15)]


metric_file.write("#t\tPDR\tLatency\tEnergy\tOverhead\t\n")

for t in delivery_times:
    avg_pdr, avg_latency, avg_energy, overhead = compute_metrics(lines, total_messages, t)
    band_usage = compute_band_usage(lines, t, del_spec_lines)
    metric_file.write(
        str(t) + "\t" + str(avg_pdr) + "\t" + str(avg_latency) + "\t" + str(avg_energy) + "\t" + str(overhead) + "\t" +
        str(band_usage[0]) + "\t" + str(band_usage[1]) + "\t" + str(band_usage[2]) + "\t" + str(band_usage[3]) + "\n")

metric_file.close()