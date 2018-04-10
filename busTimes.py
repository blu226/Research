from map_plot import *
from computeHarvesine import *
from pathlib import Path
import csv

busIDs = ["3027", "3028", "3029", "3030", "3031", "3032", "3033", "3034", "3035", "3036", "3037", "3039", "3040", "3041", "3103", "3112", "3115", "3116", "3117", "3118", "3119", "3121", "3122", "3123", "3201", "3202", "3203", "3204", "3211","3212","3213","3214","3215"]
directory = "DateWiseRoutes"

folders = findfiles(directory)
folders.sort()
folderLen = len(folders)




#For each day
for i in range(0, folderLen, 1):
    print(str(i) + " " + str(folders[i]))
    folderPath = directory + "/" + str(folders[i]) + "/"
    fileCSV = str(folders[i]) + ".csv"
    file = open(fileCSV, "w")

    buses = findfiles(folderPath)
    buses.sort()
    num_buses = len(buses)
    titleStr = str(folders[i])
    for num in range(num_buses):
        titleStr += "," + busIDs[num] + " X," + busIDs[num] + " Y"
    titleStr += "\n"

    file.write(titleStr)

    hour = 6
    min = 30

    #For a certain amount of time (each loop is 5 minutes)
    while hour < 24:
        fileStr = str(hour) + ":" + str(min)
    #For each bus
        for j in range(0, num_buses, 1):

            busFilePath = folderPath + str(buses[j])

            busFile = open(busFilePath, "r")

            timeFound = True

            for line in busFile:
                linestr = line.strip()
                linestr = linestr.split("  ")

                data = linestr[1].split(" ")
                time = data[0]
                busHour = int(time[0:2])
                busMin = int(time[3:5])

                if hour == busHour and min == busMin and timeFound:
                    timeFound = False
                    X = data[1]
                    Y = data[2]

                    fileStr += "," + X + "," + Y

            if timeFound:
                fileStr += "," + "-" + "," + "-"

            busFile.close()

        fileStr += "\n"
        file.write(fileStr)
        #print(fileStr)
        if min == 59:
            min = 0
            hour += 1
        else:
            min += 1

    file.close()



