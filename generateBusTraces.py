import os
import numpy
import random
from constants import *
from math import radians, cos, sin, asin, sqrt, inf
import pickle

def printMAT(adj):
    print("i j s ts te")
    for i in range(len(adj)):
        for j in range(len(adj[0])):
            for s in range(len(adj[0][0])):
                for ts in range(len(adj[0][0][0])):
                    for te in range(len(adj[0][0][0][0])):
                        if (adj[i, j, s, ts, te] != inf):
                            print(str(i) + " " + str(j) + " " + str(s) + " " + str(ts) + " " + str(te) + " = " + str(adj[i, j, s, ts, te]))

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    #print("lon1: " + str(lon1) + " lat1: " + str(lat1) + " lon2: " + str(lon2) + " lat2: " + str(lat2) )

    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    # Radius of earth in kilometers is 6371
    km = 6371* c
    # print(" dist: " + str(km))
    return km

def getPath():
    pathToFolder = "DieselNet-2007/gps_logs"


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
def writeToFile(folder, file, allLines):
    if not os.path.exists(folder):
        os.makedirs(folder)

    with open(folder + "/" +file, "w") as fw:
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
            fw.write(newString + "\n")

    fw.close()

def dateWiseRoutes(directory):
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
                writeToFile("Routes/" + currFiles[fInd], folders[ind], currPath)

def CHECK_IF_LINK_EXISTS(filepath1, filepath2, s, ts, te):

    with open(filepath1) as f1:
        linesInFile1 = f1.readlines()
    f1.close()

    with open(filepath2) as f2:
        linesInFile2 = f2.readlines()
    f2.close()

    currIndexInFile1 = 0
    currIndexInFile2 = 0
    currTimeInFile1 = float(linesInFile1[0].split()[0])
    currTimeInFile2 = float(linesInFile2[0].split()[0])

    # print("ts: " + str(ts) + " te: " + str(te))
    # print("First timestamp: " + str(currTimeInFile1) + " " + str(currTimeInFile2))

    # Go to ts - Skip all other lines up to ts
    while currTimeInFile1 < ts and currIndexInFile1 < len(linesInFile1):
        currIndexInFile1 += 1
        currTimeInFile1 = float(linesInFile1[currIndexInFile1].split()[0])

    # # Go to ts - Skip all other lines up to ts
    while currTimeInFile2 < ts and currIndexInFile2 < len(linesInFile2):
        currIndexInFile2 += 1
        currTimeInFile2 = float(linesInFile2[currIndexInFile2].split()[0])

    # Check if these two buses are in range between time period [ts, te]
    while currTimeInFile1 < te and currTimeInFile2 < te and currIndexInFile1 < len(
            linesInFile1) and currIndexInFile2 < len(linesInFile2):

        line1Arr = linesInFile1[currIndexInFile1].split()
        line2Arr = linesInFile2[currIndexInFile2].split()

        # print("Here: " + str(currTimeInFile1) + " " + str(currTimeInFile2))
        if haversine(float(line1Arr[3]), float(line1Arr[2]), float(line2Arr[3]), float(line2Arr[2])) > spectRange[s]:
            return False

        currIndexInFile1 += 1
        currIndexInFile2 += 1
        currTimeInFile1 = float(line1Arr[0])
        currTimeInFile2 = float(line2Arr[0])

    return True


def createLinkExistenceADJ(directory):
    folders = findfiles(directory)
    folders.sort()
    # For day 1
    currFolder = folders[0]
    fileList = findfiles(directory+ "/" + currFolder)
    fileList.sort()
    noOfFiles = len(fileList)
    noOfFiles = 6

    #T = [10 am to 12:00 pm]
    tau = 5
    scale = 600

    print("ts te i j s")
    for ts in range(0, 60 - tau, tau):
        # for te in range(ts + tau, 20, tau):
        te = ts + tau
        for i in range(0, noOfFiles, 1):
            for j in range(0, noOfFiles, 1):
                for s in range(S):

                    ts_tau = int(ts/tau)
                    te_tau = int(te/tau)

                    if i == j:
                        LINK_EXISTS[i, j, s, ts_tau, te_tau] = 1
                    else:
                        filepath1 = directory+ "/" + currFolder + "/" + fileList[i]
                        filepath2 = directory+ "/" + currFolder + "/" + fileList[j]
                        # print("ts: " + str(ts) + " te: " + str(te) + " i: " + fileList[i] + " j: " + fileList[j] + " s: " + str(s))
                        if CHECK_IF_LINK_EXISTS(filepath1, filepath2, s, float(ts + scale), float(te + scale)) == True:
                            LINK_EXISTS[i, j, s, ts_tau, te_tau] = 1

                    print(str(ts_tau) + " " + str(te_tau) + " " + str(i) + " " + str(j) + " " + str(s) + " " + str(LINK_EXISTS[i, j, s, ts_tau, te_tau]))

LINK_EXISTS = numpy.empty(shape=(50, 50, 3, 120, 120))
LINK_EXISTS.fill(inf)


directory = "DieselNet-2007/gps_logs"
#ONE TIME RUN
# dateWiseRoutes(directory)

createLinkExistenceADJ("Routes")
LE_file = open("LINK_EXISTS.txt", 'wb')
pickle.dump(LINK_EXISTS, LE_file)
LE_file.close()
print("Size of Link Exists: " + str(len(LINK_EXISTS)) + " " + str(len(LINK_EXISTS[0])) + " " + str(len(LINK_EXISTS[0][0])) + " " + str(len(LINK_EXISTS[0][0][0])))
# printMAT(LINK_EXISTS)