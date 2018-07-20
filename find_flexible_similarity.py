from STB_help import *
import numpy
import os
import shutil
import math

def find_index(t, lines):
    index = 0
    line_arr = lines[index].strip().split()
    time = float(line_arr[0])

    while time < t and index < len(lines) - 1:
        index += 1
        line_arr = lines[index].strip().split()
        time = float(line_arr[0])

    x = int(float(line_arr[2]))

    if x == 0:
        while time == t and x == 0  and index < len(lines) - 1:
            index += 1
            line_arr = lines[index].strip().split()
            time = float(line_arr[0])
            x = int(float(line_arr[2]))

    if time == t:
        return index
    else:
        return -1

def create_time_arr(lines, startTime, sim_length):

    coord_arr = []

    for i in range(startTime, startTime + sim_length):

        index = find_index(i, lines)

        if index == -1:
            coord_arr.append([-1,-1])
        else:
            line_arr = lines[index].strip().split()
            coord = [line_arr[2], line_arr[3]]
            coord_arr.append(coord)

    return coord_arr

def write_to_file(bus_file, similarity, startTime, filename, rows, rows2, sim_len):

    bus_arr = bus_file.split('.')
    busID = bus_arr[0]
    messageLine = str(busID) + "\t\t" + str(startTime) + "\t\t\t" + str(sim_len) + "\t\t" + str(similarity) + "\t\t\t" + str(rows) + '\t\t' + str(rows2) + "\n"

    f = open(filename, 'a')
    f.write(messageLine)
    f.close()

def copy_dataMule(busID, day, new_busID):

    destFolder = "DataMules/" + day + "/"
    if not os.path.exists(destFolder):
        os.makedirs(destFolder)

    curr_dir = "DateWiseRoutes/" + day + "/" + busID
    new_dir = destFolder + str(new_busID) + ".txt"

    print("Old:", curr_dir, "New:", new_dir)

    shutil.copyfile(curr_dir, new_dir)

def sort_bus_sims_max(bus_arr):

    new_bus_arr = []

    while len(bus_arr) > 0:

        max = 0
        max_ind = -1

        for i in range(len(bus_arr)):
            sim = bus_arr[i][1]
            if sim > max:
                max = sim
                max_ind = i

        new_bus_arr.append(bus_arr[max_ind])
        bus_arr.remove(bus_arr[max_ind])

    return new_bus_arr

def sort_bus_sims_min(bus_arr):

    new_bus_arr = []

    while len(bus_arr) > 0:

        min = math.inf
        min_ind = -1

        for i in range(len(bus_arr)):
            sim = bus_arr[i][1]
            if sim < min:
                min = sim
                min_ind = i

        new_bus_arr.append(bus_arr[min_ind])
        bus_arr.remove(bus_arr[min_ind])

    return new_bus_arr


#MAIN
similarity_restraint = 500 #meters
simulation_length = 180
similarity_min = -1
offset = 10

directory = "DateWiseRoutes/"
# days = os.listdir(directory)
# days = ["2007-10-31", "2007-11-01", "2007-11-06", "2007-11-07"]
days = ["2007-11-06"]
# days.sort()


for day in days:

    bus_sims = []

    filename = "Similarity_Files/bus_similarities_" + str(day) + ".txt"
    f = open(filename, 'w')
    f.write("Bus ID\t\tStart Time\tSim Len\tSimilarity\t\tNum Rows1\t\tNum Rows2\n")
    f.close()

    path = directory + day + "/"

    buses = findfiles(path)
    buses.sort()

    for startTime in range(660, 840, 180):

        f = open(filename, 'a')
        f.write("===================================================================================\n")
        f.close()

        num_valid_buses = 0
        new_busID = 9

        for bus_file in buses:

            with open(path + bus_file, 'r') as f:
                lines = f.readlines()

            bus_round1 = create_time_arr(lines, startTime, simulation_length)
            bus_round2 = create_time_arr(lines, startTime + simulation_length, simulation_length)

            similar = 0
            num_rows_w_data = 0
            num_rows_w_data_round2 = 0

            for i in range(simulation_length):

                if bus_round2[i][0] != -1:
                    num_rows_w_data_round2 += 1

                if bus_round1[i][0] != -1:

                    num_rows_w_data += 1
                    round_2_coord = []
                    distances = []

                    for j in range(i - offset, i + offset + 1):
                        if j >= simulation_length:
                            j = simulation_length -1

                        if bus_round2[j][0] != -1:
                            round_2_coord.append(bus_round2[j])

                    for j in range(len(round_2_coord)):
                        dist = funHaversine(float(bus_round1[i][1]), float(bus_round1[i][0]), float(round_2_coord[j][1]), float(round_2_coord[j][0]))
                        distances.append(dist)

                    for dist in distances:
                        if dist < similarity_restraint:
                            similar += 1
                            break

            if num_rows_w_data > 0 and num_rows_w_data_round2 > 0:
                similarity = round((similar / min(num_rows_w_data, num_rows_w_data_round2)) * 100, 2)
            else:
                similarity = 0

            if num_rows_w_data > 0.5 * simulation_length and num_rows_w_data_round2 > 0.5 * simulation_length and similarity > 30:
                write_to_file(bus_file, similarity, startTime, filename, num_rows_w_data, num_rows_w_data_round2, simulation_length)
                # copy_dataMule(bus_file, day, new_busID)
                bus_sims.append([bus_file, similarity])


    sorted_bus_sims = sort_bus_sims_min(bus_sims)


    for bus in sorted_bus_sims:
        copy_dataMule(bus[0], day, new_busID)
        new_busID += 1


    for i in sorted_bus_sims:
        print("Bus:", i[0], "Sim:", i[1])

