import os
import numpy
import random
from constants import *
from math import radians, cos, sin, asin, sqrt, inf

def findfiles(directory):
    # if directory is not 'DieselNet-2007/gps_logs/.DS_Store':
    print (directory)
    objects = os.listdir(directory)  # find all objects in a dir

    files = []
    for i in objects:  # check if very object in the folder ...
        if isFile(directory + i):  # ... is a file.
            files.append(i)  # if yes, append it.
    return files

def isFile(object):
    try:
        os.listdir(object)  # tries to get the objects inside of this object
        return False  # if it worked, it's a folder
    except Exception:  # if not, it's a file
        return True

def readFile(fileName, busName):
    allLines = []
    with open(fileName) as f:
        listOfLines = f.readlines()
        for line in listOfLines:
            line = line.strip()
            allLines.append(line)
    f.close()

    return allLines

#Append spectrum bandwidths to each gps location of each bus
def writeToFile(folder, file, allLines, startTime, endTime):
    if not os.path.exists(folder):
        os.makedirs(folder)

    with open(folder + "/" +file + ".txt", "w") as fw:
        for line in allLines:
            # Add spectrum bandwidths
            specBW = [random.randrange(minBW[s], maxBW[s]) for s in range(S)]

            lineStr = line.split(" ")
            time = lineStr[0].split(":")
            timeInMinutes = float(time[0]) * 60 + float(time[1])
            # print("Line " + lineStr[0] + " " + str(timeInMinutes))

            newString = str(timeInMinutes) + "  " + line
            for sBW in specBW:
                newString += "   " + str(sBW) + "  "

            if timeInMinutes >= startTime and timeInMinutes <= endTime:
                fw.write(newString + "\n")

    fw.close()

def busWiseRoutes(directory, startTime, endTime):
    folders = findfiles(directory)

    # print (folders)
    for ind in range(len(folders)):
        if '.DS_Store' not in folders[ind]:
            print("Bus ID: ", folders[ind])

            folderPath = directory + "/" + str(folders[ind])
            currFiles = findfiles(folderPath)
            numOfFiles = len(currFiles)
            #numOfFiles = 1
            for fInd in range(0, numOfFiles):
                print("Day: ", currFiles[fInd])
                filePath = folderPath + "/" + currFiles[fInd]
                currPath = readFile(filePath, folders[ind] + "_" + currFiles[fInd])
                writeToFile("BusWiseRoutes/" + folders[ind], currFiles[fInd], currPath, startTime, endTime)


directory = "DieselNet-2007/gps_logs"
#ONE TIME RUN

startTime = 600
endTime = 720
busWiseRoutes(directory, startTime, endTime)
