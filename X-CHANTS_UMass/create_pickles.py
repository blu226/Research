import os
import pickle
from constants import *


def get_dataMule_ID(filename):
    if filename[1] == '.':
        return filename[0]
    else:
        return filename[0:2]



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


# days = os.listdir("../DataMules/")
# days.sort()
# directorys = ['2007-10-23_2007-10-24/', '2007-10-24_2007-10-25/', '2007-10-25_2007-10-26/', '2007-10-26_2007-10-27/','2007-10-29_2007-10-30/','2007-10-30_2007-10-31/','2007-10-31_2007-11-01/','2007-11-01_2007-11-02/','2007-11-02_2007-11-03/','2007-11-03_2007-11-04/','2007-11-04_2007-11-05/','2007-11-05_2007-11-06/','2007-11-06_2007-11-07/','2007-11-07_2007-11-08/','2007-11-09_2007-11-10/','2007-11-10_2007-11-11/']
# startTime = [800,800,680,920,680,920,680,920,680,560,800,560,680,560,800,560,800,560]
days = ["2"]
directorys = ['2007-11-06/']
startTime = [840]

for i in range(len(directorys)):

    for day in days:
        dataMules = os.listdir("../DataMules/" + directorys[i] + "/Day" + day + "/")
        dataMules.sort()
        print(dataMules)

        for bus in dataMules:

            if not os.path.exists("../DataMules/" + directorys[i] + "/Day" + day + "_pkl/" ):
                os.makedirs("../DataMules/" + directorys[i] + "/Day" + day + "_pkl/" )

            coord_at_time = []

            with open("../DataMules/" + directorys[i] + "Day" + day + "/" + bus, 'r') as f:
                lines = f.readlines()
            f.close()

            file_len = len(lines)



            for t in range(startTime[i], startTime[i] + T + 1):

                index = find_index(t, lines)
                if index != -1:
                    line_arr = lines[index].strip().split()
                    coord = [line_arr[2], line_arr[3]]
                else:
                    coord = [-1, -1]

                coord_at_time.append(coord)

            filename = get_dataMule_ID(bus)
            filename = filename + ".pkl"

            # print(coord_at_time)

            pickle_file = open("../DataMules/" + directorys[i] + "/Day" + day + "_pkl/" + filename, 'wb')
            pickle.dump(coord_at_time, pickle_file, protocol=4)
            pickle_file.close()





