from map_plot import *
from computeHarvesine import *
from pathlib import Path

def printTimes(times):
    if len(times) == 0:
        print("none")
    else:
        for i in range(len(times)):
            print(str(times[i]))

directory = "DieselNet-2007/gps_logs"
#generateData(directory)

folders = findfiles(directory)
folders.sort()

folderLen = len(folders)

#For each bus
for ind in range(0, folderLen, 1):
    #if ".DS_Store" not in folders:
       # print("Current Folder " + folders[ind])

    print("Bus: " + str(folders[ind]))
    folderPath = directory + "/" + str(folders[ind]) + "/2007-10-23"

    if Path(folderPath).is_file():

        file = open(folderPath, "r")

        startX = 42.387142
        startY = -72.526355

        endX = 42.254215
        endY = -72.577024

        startTimes = []
        endTimes = []

        for line in file:

            linestr = line.strip()
            linestr = linestr.split(" ")

            curTime = linestr[0]
            curX = float(linestr[1])
            curY = float(linestr[2])

            distS = funHaversine(curX,curY,startX,startY)
            distE = funHaversine(curX,curY,endX,endY)

            if distS < .05:
                #print("Within 100m of START at time: " + curTime)
                startTimes.append(curTime)
            elif distE < .05:
                #print("Within 100m of END at time: " + curTime)
                endTimes.append(curTime)

        print("START TIMES")
        printTimes(startTimes)
        print("END TIMES")
        printTimes(endTimes)
        print()
        file.close()

    else:
        print("No data for this day\n")