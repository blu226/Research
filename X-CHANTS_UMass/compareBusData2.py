from STB_help import findfiles
from computeHarvesine import *
import numpy as np
import os
import shutil
from constants import *

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

        day1_dest = destFolder1 + "/" + str(i + NoOfSources + NoOfDataCenters) + ".txt"
        day2_dest = destFolder2 + "/" +str(i+ NoOfSources + NoOfDataCenters) + ".txt"

        shutil.copyfile(day1_filePath, day1_dest)
        shutil.copyfile(day2_filePath, day2_dest)


def getIndex(ts, currTimeInFile1, currTimeInFile2, currIndexInFile1, currIndexInFile2, linesInFile1, linesInFile2):
    while currTimeInFile1 < ts and currIndexInFile1 < len(linesInFile1) - 1:
        currIndexInFile1 += 1
        currTimeInFile1 = float(linesInFile1[currIndexInFile1].split()[0])

    # # Go to ts - Skip all other lines up to ts
    while currTimeInFile2 < ts and currIndexInFile2 < len(linesInFile2) - 1:
        currIndexInFile2 += 1
        currTimeInFile2 = float(linesInFile2[currIndexInFile2].split()[0])

    return currIndexInFile1, currIndexInFile2

#
directory = "../DataMules/"
days = os.listdir(directory)
days.sort()


for file in days:
# directory1 = "DataMules/2007-11-03_2007-11-04/Day1"
# directory2 = "DataMules/2007-11-03_2007-11-04/Day2"
#
# directory1 = "DataMules/2007-10-23_2007-10-25/Day1"
# directory2 = "DataMules/2007-10-23_2007-10-25/Day2"

    if file == "2007-10-31_2007-11-01":
        directory1 = directory + file + "/Day1"
        directory2 = directory + file + "/Day2"
        folders = findfiles(directory1)
        folders.sort()
        folderLen = len(folders)


        times = []
        ratios = []
        for time in range(400, 1000, 50):

            total_row = 0
            total_sim = 0

            for first_file in range(folderLen):
                if folders[first_file] not in ["0.txt","1.txt","2.txt","3.txt","4.txt","5.txt", "6.txt", "7.txt", "8.txt"]:




                    file1 = directory1 + "/" + str(folders[first_file])  #2007-10-23
                    file2 = directory2 + "/" + str(folders[first_file]) #2007-11-06


                    numRows = 0
                    rowSimilar = 0

                    # if folders[first_file] != "2007-11-03.csv" and folders[second_file] != "2007-11-04.csv":
                    #     break

                    with open(file1, "r") as f:
                        day1_lines = f.readlines()[1:]

                    with open(file2, "r") as f:
                        day2_lines = f.readlines()[1:]

                    ind1 = 0
                    ind2 = 0
                    time1 = float(day1_lines[ind1].split()[0])
                    time2 = float(day2_lines[ind2].split()[0])
                    for i in range(120):
                        ind1, ind2 = getIndex(time + i, time1, time2, ind1, ind2, day1_lines, day2_lines)
                        time1 = float(day1_lines[ind1].split()[0])
                        print(ind2)
                        time2 = float(day2_lines[ind2].split()[0])

                        if (time1 == float(time + i)  and time2 == float(time + i)):
                            #print(currTimeInFile1, currTimeInFile2, ts)
                            line_arr1 = day1_lines[ind1].split()
                            line_arr2 = day2_lines[ind2].split()

                            X1 = line_arr1[2]
                            Y1 = line_arr1[3]
                            X2 = line_arr2[2]
                            Y2 = line_arr2[3]
                            numRows += 1
                            if (X1 != "-" and X1 != "0.0" and X2 != "-" and X2 != "0.0"):


                                dist = funHaversine(float(Y1), float(X1), float(Y2), float(X2))
                        #                print(dist)
                                if dist < 1000 and dist >= 0:
                                    rowSimilar += 1


                    total_row += numRows
                    total_sim += rowSimilar

                    # if str(folders[first_file]) not in ["0.txt","1.txt","2.txt","3.txt","4.txt","5.txt", "6.txt", "7.txt", "8.txt"]:
                        # print(str(folders[first_file]))

                       # else:
                            # print("NumRows:", str(numRows),"\nRowsSimilar: ", str(rowSimilar),"\nSimilarity: ", str(100*rowSimilar/numRows), "\n")
                            #sum += rowSimilar
            if total_row > 100:
                ratio = total_sim/total_row
                if ratio > 0:
                    times.append(time)
                    ratios.append(ratio)
                   # print(directory1)
                    print(str(time) + ": " + str(ratio*100)[:4] + " " + str(total_row))
        # #
        if len(ratios) > 0:
            max_ratio = min(ratios)
            index = ratios.index(max_ratio)
            print(str(times[index]) + ": " + str(max_ratio*100)[:4])

        f = open("Similarity_Ratios.txt", "a")

        print("---------------------------------------------------------------\n")
        print("Days: " + str(folders[first_file]) + " and " + str(folders[second_file]))
        print("i\tj\tNumRows\tSimilarity")

        f.write("---------------------------------------------------------------\n")
        f.write("Days: " + str(folders[first_file]) + " and " + str(folders[second_file]) + "\n")
        f.write("i\tj\tNumRows\tSimilarity\n")



       # moveFiles(day1_buses, day2_buses, similarity, str(folders[first_file]), str(folders[second_file]))