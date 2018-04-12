import re
import random
import os
import numpy
import pickle

from constants import *
from math import radians, cos, sin, asin, sqrt, inf


def funHaversine(lon1, lat1, lon2, lat2):
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


def save_in_file(adj):
    with open("LINK_EXISTS_file.txt", "w") as f:
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


def printMAT(adj):
    print("i j s ts te")
    for i in range(len(adj)):
        for j in range(len(adj[0])):
            for s in range(len(adj[0][0])):
                for ts in range(len(adj[0][0][0])):
                    for te in range(len(adj[0][0][0][0])):
                        if (adj[i, j, s, ts, te] != inf and i != j):
                            print(str(i) + " " + str(j) + " " + str(s) + " " + str(ts) + " " + str(te) + " = " + str(adj[i, j, s, ts, te]))


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

def readTrajectoryFile(DMTrajectories):
    files = findfiles("Lexington/")
    if ".DS_Store" in files:
        files.remove(".DS_Store")
    files.sort()
    for file in files:
        filepath = "Lexington/"+ file
        print("Current file: " + file)
        with open(filepath) as fp:
            lines = fp.readlines()

            for index in range(0, len(lines)):
                patternMatch = re.match(r'^LINESTRING \((.*)\)', lines[index], re.M | re.I)

                if patternMatch:
                    # print ("Pattern 1: ", patternMatch.group(1))
                    trajectoryCoord = patternMatch.group(1)
                    DMTrajectories.append(trajectoryCoord.strip().split(','))

                else:
                    print ("No Match !!!")
    fp.close()

def euclideanDistance(coor1X, coor1Y, coor2X, coor2Y):
    return (sqrt((float(coor1X) - float(coor2X))**2 + (float(coor1Y) - float(coor2Y))**2))
    # return funHaversine(float(currCoors[1]), float(currCoors[0]), float(prevCoors[1]), float(prevCoors[0]))


def getLocationsOfSourcesAndDataCenters(startIndex, endIndex):
    # create file for Sources. Though the source location are fixed, the spectrum bandwidth changes over time
    # Hence, it is important to save it as a file

    for srcID in range(startIndex, endIndex, 1):

        villageCoor = random.choice(DMTrajectories[srcID%len(DMTrajectories)])
        srcLocationX = villageCoor.strip().split(" ")[0]
        srcLocationY = villageCoor.strip().split(" ")[1]
        print("Location: " + villageCoor + " " + srcLocationX + " " + srcLocationY)

        with open(directory + "/" + str(srcID) + ".txt", "w") as srcP:
            srcP.write("T X Y ")
            for s in range(S):
                srcP.write("S" + str(s) + " ")
            srcP.write("\n")

            for t in range(0, T, dt):
                srcP.write(str(t) + " " + str(srcLocationX) + " " + str(srcLocationY) + " ")

                # Change the bandwidth of each spectrum at each DSA node at each time epoch
                specBW = [random.randrange(minBW[s], maxBW[s]) for s in range(S)]
                # print ("Length of spectrum: " + str(S))
                for sBW in specBW:
                    srcP.write(str(sBW) + " ")
                srcP.write("\n")
        srcP.close()


def getLocationsOfDMs(DMTrajectories, startIndex, endIndex):
    # Generate a random yet unique speed for each data mule
    #DMSpeed = [random.randint(VMIN, VMAX) for i in range(len(DMTrajectories))]
    dmID = startIndex - 1

    for ind in range(startIndex, endIndex, 1):
        dmID = dmID + 1
        currTime = random.randint(route_start_time1, route_start_time2)
        currCoorID = 0
        nextCoorID = 1

        dmSpeed = random.randint(VMIN, VMAX)
        # dmSpeed = 50

        # if dmID >= endIndex:
        #     break
        chosen_trajectory_id = random.randint(0, len(DMTrajectories)-1)
        eachDM = DMTrajectories[chosen_trajectory_id]

        print("Trajectory " +  str(len(eachDM)) + " : " + str(eachDM))

        with open(directory + "/"+ str(dmID)+".txt", "w") as dmP:
            print ("For DM: " + str(dmID) + " Speed: " + str(dmSpeed))
            dmP.write("T X Y ");
            for s in range(S):
                dmP.write("S"+ str(s) + " ")
            dmP.write("\n")

            # By default, move in the forward direction
            isDirectionForward = True

            for t in range(currTime, T, dt):
                prevCoors = eachDM[currCoorID].strip().split(' ')
                currCoors = eachDM[nextCoorID].strip().split(' ')

                consumedTime = euclideanDistance(prevCoors[0], prevCoors[1], currCoors[0], currCoors[1])/dmSpeed
                # print("Curr " + str(currCoorID) + " Next " + str(nextCoorID) + " consTime: " + str(consumedTime))

                if consumedTime > t or t == T- dt:
                    # Stay in the same location
                    # print (str(t) + " " + str(eachDM[currCoorID]))
                    dmP.write(str(t) + " " + eachDM[currCoorID].strip() + " ")

                else:
                    # Move to the next location
                    dmP.write(str(t) + " " + eachDM[nextCoorID].strip() + " ")

                    #Set the current ID and next ID appropriately
                    currCoorID = nextCoorID

                    #repeat from start of the trajectory (if currently at the end of the trajectory)
                    # Each trajectory is periodic
                    if currCoorID == len(eachDM) - 1:
                        isDirectionForward = False

                    if currCoorID == 0:
                        isDirectionForward = True

                    if isDirectionForward:
                        nextCoorID = currCoorID + 1

                    else:
                        nextCoorID = currCoorID - 1

                # Change the bandwidth of each spectrum at each DSA node at each time epoch
                specBW = [random.randrange(minBW[s], maxBW[s]) for s in range(S)]
                # print ("Length of spectrum: " + str(S))
                for sBW in specBW:
                    dmP.write(str(sBW) + " ")
                dmP.write("\n")
        dmP.close()


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
    print("ts te i j s")
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

dt = 1
# This function is independent of tau
LINK_EXISTS = numpy.empty(shape=(V, V, S, int(T/dt), int(T/dt)))
LINK_EXISTS.fill(inf)

#filepath = 'Data/trajectory.txt'
directory = "Lexington/Day1"
if not os.path.exists(directory):
    os.makedirs(directory)

DMTrajectories = []         #stores the coordinates for each data mule

# Read trajectory for each data mule
readTrajectoryFile(DMTrajectories)
selectedDMTrajectories = DMTrajectories[:5]

print("Length of DM trajectories: ", len(DMTrajectories))
print("Length of Selected DM trajectories: ", len(selectedDMTrajectories))

# Randomly place sources (index from 0 to S -1)
getLocationsOfSourcesAndDataCenters(0, NoOfSources)

# Place DMs on selected Routes (index from (S - DM)
getLocationsOfDMs(selectedDMTrajectories, NoOfSources, NoOfSources + NoOfDMs)

# Randomly place data centers (index from (DM -  DM + D))
getLocationsOfSourcesAndDataCenters(NoOfSources + NoOfDMs, (NoOfSources + NoOfDMs + NoOfDataCenters ))

# createLinkExistenceADJ("Lexington")
# LE_file = open("LINK_EXISTS_pickle.txt", 'wb')
# pickle.dump(LINK_EXISTS, LE_file)
# LE_file.close()
#
# print("Size of Link Exists: " + str(len(LINK_EXISTS)) + " " + str(len(LINK_EXISTS[0])) + " " + str(len(LINK_EXISTS[0][0])) + " " + str(len(LINK_EXISTS[0][0][0])))
# save_in_file(LINK_EXISTS)
#printMAT(LINK_EXISTS)