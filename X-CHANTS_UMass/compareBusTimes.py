from STB_help import *
from computeHarvesine import *
import numpy as np
import os
import shutil

directory = "../DataMules/2007-11-04_2007-11-05/Day1/"
time_in_range = 10

folders = findfiles(directory)
folders.sort()
folderLen = len(folders)

stops = []

for first_file in range(7):

    file = directory + folders[first_file]



    with open(file, "r") as f:
        day_lines = f.readlines()

    for i in range(len(day_lines)-1):
        day_line = day_lines[i].strip()
        day1_line_arr = day_line.split()

        time = day1_line_arr[0]
        x1 = day1_line_arr[2]
        y1 = day1_line_arr[3]

        ind = 1
        next_line = day_lines[i+ind]
        next_line = next_line.strip()
        next_line_arr = next_line.split()
        time2 = next_line[0]
        while float(time2) != float(time) + time_in_range and (i + ind) < len(day_lines):
            next_line = day_lines[i + ind]
            next_line = next_line.strip()
            next_line_arr = next_line.split()
            time2 = next_line_arr[0]
            ind += 1

        if float(time2) == float(time) + time_in_range and float(time2) > 849 and float(time2) < 971:
            x2 = next_line_arr[2]
            y2 = next_line_arr[3]

            dist = funHaversine(float(y1),float(x1),float(y2),float(x2))
            #print(dist)
            if dist <= 10:
                stops.append([x1,y1])

#print(stops)
coords = []
for i in range(len(stops)):
    coord1 = stops[i]
    x1 = coord1[0]
    y1 = coord1[1]
    for j in range(len(stops)):
        coord2 = stops[j]
        x2 = coord2[0]
        y2 = coord2[1]

        dist = funHaversine(float(y1),float(x1),float(y2),float(x2))
        #print(dist)
        if dist > 2000:
            if len(coords) == 0:
                coords.append([x1,y1])
                coords.append([x2,y2])
            else:
                dist2_flag = True
                dist3_flag = True
                for i in range(len(coords)):
                    x = coords[i][0]
                    y = coords[i][1]

                    dist2 = funHaversine(float(y), float(x), float(y1), float(x1))
                    dist3 = funHaversine(float(y), float(x), float(y2), float(x2))

                    if dist2 < 5:
                        dist2_flag = False
                    if dist3 < 5:
                        dist3_flag = False

                if dist2_flag == True:
                    coords.append([x1,y1])
                if dist3_flag == True:
                    coords.append([x2,y2])

for x in coords:
    print(str(x[0]), str(x[1]))