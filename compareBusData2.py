from map_plot import findfiles
from computeHarvesine import *
import numpy as np

directory = "DateWiseRoutes_CSV"

folders = findfiles(directory)
folders.sort()
folderLen = len(folders)

file1 = directory + "/" + str(folders[0])  #2007-10-23
file2 = directory + "/" + str(folders[14]) #2007-11-06

with open(directory +"/" + str(folders[0]), "r") as f:
    day1_lines = f.readlines()[1:]

with open(directory +"/" + str(folders[14]), "r") as f:
    day2_lines = f.readlines()[1:]

rowSimilar = np.zeros(shape=(30, 28))
numRows = np.zeros(shape=(30,28))

common_line_len = min(len(day1_lines), len(day2_lines))

day1_bus = -1

for i in range(1, 61, 2):

    day1_bus += 1
    day2_bus = -1

    for j in range(1, 57, 2):

        day2_bus += 1

        for ind in range(common_line_len):


            day1_line = day1_lines[ind].strip()
            day1_line_arr = day1_line.split(",")

            day2_line = day2_lines[ind].strip()
            day2_line_arr = day2_line.split(",")

            X1 = day1_line_arr[i]
            Y1 = day1_line_arr[i+1]

            X2 = day2_line_arr[j]
            Y2 = day2_line_arr[j+1]

#            print("X1: " + str(X1) + " Y1: " + str(Y1) + " X2: " + str(X2) + " Y2: " + str(Y2))

            if (X1 != "-" and X1 != "0.0" and X2 != "-" and X2 != "0.0"):

                numRows[day1_bus][day2_bus] += 1
                dist = funHaversine(float(X1), float(Y1), float(X2), float(Y2))
#                print(dist)
                if dist < .1 and dist > 0:
                    rowSimilar[day1_bus][day2_bus] += 1

print("i\tj\tNumRows\tSimilarity")

for i in range(30):
    for j in range(28):

        if numRows[i][j] != 0 and numRows[i][j] > 100:
            ratio = (rowSimilar[i][j]/numRows[i][j]) * 100
            if ratio > 10:
                print(str(i) + "\t" + str(j) + "\t" + str(numRows[i][j]) + "\t" + str(ratio) + "%")
