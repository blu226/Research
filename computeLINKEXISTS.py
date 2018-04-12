import re
import random
import os
import numpy
import pickle
from constants import *
from math import radians, cos, sin, asin, sqrt, inf


def isFile(object):
    try:
        os.listdir(object)  # tries to get the objects inside of this object
        return False  # if it worked, it's a folder
    except Exception:  # if not, it's a file
        return True


def findfiles(directory):
    # if directory is not 'DieselNet-2007/gps_logs/.DS_Store':
    print (directory)
    objects = os.listdir(directory)  # find all objects in a dir

    files = []
    for i in objects:  # check if very object in the folder ...
        if isFile(directory + i):  # ... is a file.
            files.append(i)  # if yes, append it.
    return files

def euclideanDistance(coor1X, coor1Y, coor2X, coor2Y):
    return (sqrt((float(coor1X) - float(coor2X))**2 + (float(coor1Y) - float(coor2Y))**2))
    # return funHaversine(float(currCoors[1]), float(currCoors[0]), float(prevCoors[1]), float(prevCoors[0]))


def save_in_file(filename, adj):
    with open(path_to_folder + filename, "w") as f:
        f.write("i j s ts te")
        for i in range(len(adj)):
            for j in range(len(adj[0])):
                for s in range(len(adj[0][0])):
                    for ts in range(len(adj[0][0][0])):
                        for te in range(len(adj[0][0][0][0])):
                            if (adj[i, j, s, ts, te] != inf and i != j):
                                f.write(str(i) + " " + str(j) + " " + str(s) + " " + str(ts) + " " + str(te) + " = " + str(
                                        adj[i, j, s, ts, te]) + "\n")

    f.close()


def CHECK_IF_LINK_EXISTS(filepath1, filepath2, s, ts, te):

    with open(filepath1) as f1:
        linesInFile1 = f1.readlines()[1:]
    f1.close()

    with open(filepath2) as f2:
        linesInFile2 = f2.readlines()[1:]
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
        if euclideanDistance(float(line1Arr[1]), float(line1Arr[2]), float(line2Arr[1]), float(line2Arr[2])) > spectRange[s]:
            return False

        currIndexInFile1 += 1
        currIndexInFile2 += 1
        currTimeInFile1 = float(line1Arr[0])
        currTimeInFile2 = float(line2Arr[0])

    return True

def createLinkExistenceADJ(directory):
    folders = findfiles(directory)
    if ".DS_Store" in folders:
        folders.remove(".DS_Store")
    folders.sort()
    # For day 1
    currFolder = folders[0]
    fileList = findfiles(directory + "/" + currFolder)

    if ".DS_Store" in fileList:
        fileList.remove(".DS_Store")
    fileList.sort()
    noOfFiles = len(fileList)
    # noOfFiles = 10

    print("Files " + str(noOfFiles), fileList)
    print("#ts te i j s \n")
    for ts in range(0, T - dt, dt):
        te = ts + dt
        for i in range(noOfFiles):
            for j in range(noOfFiles):
                for s in range(S):

                    ts_dt = int(ts / dt)
                    te_dt = int(te / dt)

                    if i == j:
                        LINK_EXISTS[i, j, s, ts_dt, te_dt] = 1
                    else:
                        filepath1 = directory + "/" + currFolder + "/" + fileList[i]
                        filepath2 = directory + "/" + currFolder + "/" + fileList[j]
                        # print("ts: " + str(ts) + " te: " + str(te) + " i: " + fileList[i] + " j: " + fileList[j] + " s: " + str(s))
                        if CHECK_IF_LINK_EXISTS(filepath1, filepath2, s, ts, te) == True:
                            LINK_EXISTS[i, j, s, ts_dt, te_dt] = 1

                    # print(str(ts_dt) + " " + str(te_dt) + " " + str(i) + " " + str(j) + " " + str(s) + " " + str(
                    #     LINK_EXISTS[i, j, s, ts_dt, te_dt]))

# Main starts here

# This function is independent of tau
LINK_EXISTS = numpy.empty(shape=(V, V, S, int(T/dt), int(T/dt)))
LINK_EXISTS.fill(inf)

#filepath = 'Data/trajectory.txt'
directory = "Lexington/Day1"
if not os.path.exists(directory):
    os.makedirs(directory)

createLinkExistenceADJ("Lexington")

# band_type = ["ALL", "TV", "ISM"]
# path_to_folder = "Bands/" + band_type[1]+"/"

LE_file = open( path_to_folder + "LINK_EXISTS.pkl", 'wb')
pickle.dump(LINK_EXISTS, LE_file)
LE_file.close()

print("Size of Link Exists: " + str(len(LINK_EXISTS)) + " " + str(len(LINK_EXISTS[0])) + " " + str(len(LINK_EXISTS[0][0])) + " " + str(len(LINK_EXISTS[0][0][0])))
save_in_file("LINK_EXISTS.txt", LINK_EXISTS)
#printMAT(LINK_EXISTS)