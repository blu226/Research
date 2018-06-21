from STB_help import *
import numpy
import os

def find_index(t, lines):
    index = 0
    line_arr = lines[index].strip().split()
    time = float(line_arr[0])

    while time < t and index < len(lines) - 1:
        index += 1
        line_arr = lines[index].strip().split()
        time = float(line_arr[0])

    x = line_arr[2]

    if x == '0':
        while time == t and x == '0'  and index < len(lines) - 1:
            index += 1
            line_arr = lines[index].strip().split()
            time = float(line_arr[0])
            x = line_arr[2]

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

def write_to_file(bus_file, similarity, startTime, filename, rows):


    if similarity > 40:
        bus_arr = bus_file.split('.')
        busID = bus_arr[0]
        messageLine = str(busID) + "\t\t" + str(startTime) + "\t\t\t\t" + str(similarity) + "\t\t\t" + str(rows) + "\n"

        f = open(filename, 'a')
        f.write(messageLine)
        f.close()


#MAIN
simulation_length = 180
amount_of_data_needed = simulation_length * 2
similarity_restraint = 500 #meters

directory = "DateWiseRoutes/"
days = os.listdir(directory)
days.sort()


for day in days:


    filename = "Similarity_Files/bus_similarities_" + str(day) + ".txt"
    f = open(filename, 'w')
    f.write("Bus ID\t\tStart Time\t\tSimilarity\t\tNum Rows\n")
    f.close()

    path = directory + day + "/"

    buses = findfiles(path)
    buses.sort()

    print(day)
    for startTime in range(420,1200,30):

        f = open(filename, 'a')
        f.write("-----------------------------------------------------------------------------------\n")
        f.close()

        num_valid_buses = 0

        for bus_file in buses:

            with open(path + bus_file, 'r') as f:
                lines = f.readlines()

            time_begin_arr = lines[0].strip().split()
            time_end_arr = lines[len(lines) - 1].strip().split()

            time_begin = float(time_begin_arr[0])
            time_end = float(time_end_arr[0])

            # print("end ", time_end," begin ", time_begin)
            if time_end - time_begin > amount_of_data_needed:

                num_valid_buses += 1

                bus_round1 = create_time_arr(lines, startTime, simulation_length)
                bus_round2 = create_time_arr(lines, startTime + simulation_length, simulation_length)

                similar = 0
                num_rows_w_data = 0

                for i in range(simulation_length):

                    if bus_round1[i][0] != -1:
                        num_rows_w_data += 1

                    if bus_round1[i][0] != -1 and bus_round2[i][0] != -1:

                        dist = funHaversine(float(bus_round1[i][1]), float(bus_round1[i][0]), float(bus_round2[i][1]), float(bus_round2[i][0]))

                        if dist < similarity_restraint:
                            similar +=1

                if num_rows_w_data > 0:
                    similarity = round((similar / num_rows_w_data) * 100, 2)
                    write_to_file(bus_file, similarity, startTime, filename, num_rows_w_data)

        f = open(filename, 'a')
        f.write("Number of valid buses: " + str(num_valid_buses) + "\n")
        f.close()

