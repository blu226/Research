from map_plot import findfiles
from computeHarvesine import *
import numpy as np
import os
import shutil

directory = "DateWiseRoutes_CSV"

folders = findfiles(directory)
folders.sort()
folderLen = len(folders)

def moveFiles(day1, day2, similarity, day1_name, day2_name):

    day1_chosen = []
    day2_chosen = []

    while len(day1) != 0:
        maxIndex = -1
        maxSim = 0

        for i in range(len(day1)):
            if similarity[i] > maxSim:
                maxIndex = i
                maxSim = similarity[i]

        if day1[maxIndex] not in day1_chosen and day2[maxIndex] not in day2_chosen:
            day1_chosen.append(day1[maxIndex])
            day2_chosen.append(day2[maxIndex])

        day1.pop(maxIndex)
        day2.pop(maxIndex)
        similarity.pop(maxIndex)

    day1_path = "DateWiseRoutes/" + day1_name[:10]
    day1_folder = findfiles(day1_path)
    day2_path = "DateWiseRoutes/" + day2_name[:10]
    day2_folder = findfiles(day2_path)

    destFolder = "DataMules/" + day1_name[:10] + "_" + day2_name[:10]
    if not os.path.exists(destFolder):
        os.makedirs(destFolder)

    destFolder1 = destFolder + "/" + day1_name
    if not os.path.exists(destFolder1):
        os.makedirs(destFolder1)

    destFolder2 = destFolder + "/" + day2_name
    if not os.path.exists(destFolder2):
        os.makedirs(destFolder2)
    print(day1_chosen)
    for i in range(len(day1_chosen)):
        day1_file = day1_folder[day1_chosen[i]]
        day1_filePath = day1_path + "/" + day1_file
        day2_file = day2_folder[day2_chosen[i]]
        day2_filePath = day2_path + "/" + day2_file

        day1_dest = destFolder1 + "/" + str(i) + ".txt"
        day2_dest = destFolder2 + "/" +str(i) + ".txt"

        shutil.copyfile(day1_filePath, day1_dest)
        shutil.copyfile(day2_filePath, day2_dest)





for first_file in range(folderLen - 1):
    for second_file in range(first_file, folderLen - 1):
        if( first_file != second_file):

            file1 = directory + "/" + str(folders[first_file])  #2007-10-23
            file2 = directory + "/" + str(folders[second_file]) #2007-11-06

            with open(file1, "r") as f:
                day1_lines = f.readlines()[1:]

            with open(file2, "r") as f:
                day2_lines = f.readlines()[1:]

            day1_buses = []
            day2_buses = []
            similarity = []

            day1_num_buses_loop = len(day1_lines[1].split(","))
            day2_num_buses_loop = len(day2_lines[1].split(","))

            day1_num_buses = int((day1_num_buses_loop - 1)/2)
            day2_num_buses = int((day2_num_buses_loop - 1)/2)

            rowSimilar = np.zeros(shape=(day1_num_buses, day2_num_buses))
            numRows = np.zeros(shape=(day1_num_buses, day2_num_buses))

            common_line_len = min(len(day1_lines), len(day2_lines))

            day1_bus = -1

            for i in range(1, day1_num_buses_loop, 2):

                day1_bus += 1
                day2_bus = -1

                for j in range(1, day2_num_buses_loop, 2):

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
                            if dist < .2 and dist > 0:
                                rowSimilar[day1_bus][day2_bus] += 1

            f = open("Similarity_Ratios.txt", "a")

            # print("---------------------------------------------------------------\n")
            # print("Days: " + str(folders[first_file]) + " and " + str(folders[second_file]))
            # print("i\tj\tNumRows\tSimilarity")

            # f.write("---------------------------------------------------------------\n")
            # f.write("Days: " + str(folders[first_file]) + " and " + str(folders[second_file]) + "\n")
            # f.write("i\tj\tNumRows\tSimilarity\n")

            for i in range(day1_num_buses):
                for j in range(day2_num_buses):
                    if numRows[i][j] != 0 and numRows[i][j] > 100:
                        ratio = (rowSimilar[i][j]/numRows[i][j]) * 100
                        if ratio > 50:
                            # print(str(i) + "\t" + str(j) + "\t" + str(numRows[i][j]) + "\t" + str(ratio) + "%")
                            # f.write(str(i) + "\t" + str(j) + "\t" + str(numRows[i][j]) + "\t" + str(ratio) + "%\n")

                            day1_buses.append(i)
                            day2_buses.append(j)
                            similarity.append(ratio)

            f.close()


            moveFiles(day1_buses, day2_buses, similarity, str(folders[first_file]), str(folders[second_file]))