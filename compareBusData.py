from map_plot import *
from computeHarvesine import *
from pathlib import Path
import numpy as np

directory = "DateWiseRoutes_CSV"

folders = findfiles(directory)
folders.sort()
folderLen = len(folders)

#For each file, skipping first and last file, First file is the one being compared to and the last is the .ods
#for i in range(1, folderLen - 1, 1):
file1 = directory + "/" + str(folders[0])  #2007-10-23
file2 = directory + "/" + str(folders[14]) #2007-11-06
#print(file2)
# compareFile = open(file1, "r")
# file = open(file2, "r")
#
# compareFileHeader = compareFile.readline()
# fileHeader = file.readline()
#
# compareFileInfo = compareFileHeader.split(",")
# fileInfo = fileHeader.split(",")
#
# goodData = []
# badData = []


with open(directory +"/" + str(folders[0]), "r") as f:
    day1_lines = f.readlines()[1:]

with open(directory +"/" + str(folders[14]), "r") as f:
    day2_lines = f.readlines()[1:]

rowSimilar = np.zeros(shape=(35, 35))
totalRow = np.zeros(shape=(35,35))

print("Length of day1: ", len(day1_lines))

common_line_len = min(len(day1_lines), len(day2_lines))
for ind in range(common_line_len):

    #line = file.readline()
    day1_line = day1_lines[ind].strip()
    day1_line_arr = day1_line.split(",")
    day1_line_len = len(day1_line_arr)

    day2_line = day2_lines[ind].strip()
    day2_line_arr = day2_line.split(",")
    day2_line_len = len(day2_line_arr)

    day1_bus_count = -1
    day2_bus_count = -1

    for x in range(1, len(day1_line_arr), 2):

        day1_bus_count += 1
        X1 = day1_line_arr[x]                 #13     #15
        Y1 = day1_line_arr[x+1]                 #14     #16

        for y in range(1, len(day2_line_arr), 2):
            day2_bus_count += 1
            X2 = day2_line_arr[y]                     #1      #1
            Y2 = day2_line_arr[y+1]                     #2      #2

            if (X1 != "-" and X1 != "0.0" and X2 != "-" and X2 != "0.0"):

                totalRow[day1_bus_count][day2_bus_count] += 1
                dist = funHaversine(float(X1), float(Y1), float(X2), float(Y2))
                if dist < .1 and dist > 0:
                    rowSimilar[day1_bus_count][day2_bus_count] += 1

            # print(day1_line_arr[0] + " " + day1_line_arr[x] + " " + day2_line_arr[x])

for i in range(10):
    for j in range(10):
        print("Similarity Ratio:  " + str(rowSimilar[i][j]))

'''
    for k in range(1,compareLength,2):

        if (newCompare[k] != "-" and newCompare[k] != "0.0"):
            numBuses1 += 1
            compareX = float(newCompare[k])
            compareY = float(newCompare[k+1])

            numBuses2 = 0
            for j in range(1, lineLength,2):

                if (newLine[j] != "-" and newLine[j] != "0.0"):
                    numBuses2 += 1
                    lineX = float(newLine[j])
                    lineY =float(newLine[j+1])

                    dist = funHaversine(compareX, compareY, lineX, lineY)
                    #print(dist)
                    if dist < .1 and dist > 0:
                        similar = [time, dist, compareX, compareY, lineX, lineY]
                        goodData.append(similar)
                    elif dist > 0:
                        similar = [time, dist, compareX, compareY, lineX, lineY]
                        badData.append(similar)

                    if (k == compareLength -2 and j == lineLength -2):
                        print(time + ": " + str(numBuses1) + " " + str(numBuses2))
'''
'''
f = open("similar.txt", "w")
for x in goodData:
    f.write(str(x))
    f.write("\n")
f.close()
f = open("notSimilar.txt","w")
for x in badData:
    f.write(str(x))
    f.write("\n")
f.close()

# print(compareLine)
    #print(line)
'''