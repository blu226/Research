import re
import random
import os
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

def readTrajectoryFile(DMTrajectories):
    files = findfiles("Lexington/")
    files.sort()
    for file in files:
        filepath = "Lexington/"+ file
        print("Current file: " + file)
        with open(filepath) as fp:
            lines = fp.readlines()

            for index in range(0, len(lines)):
                patternMatch = re.match(r'^LINESTRING \((.*)\)', lines[index], re.M | re.I)

                if patternMatch:
                    print ("Pattern 1: ", patternMatch.group(1))
                    trajectoryCoord = patternMatch.group(1)
                    DMTrajectories.append(trajectoryCoord.strip().split(','))

                else:
                    patternMatch2 = re.match(r'^GEOMETRYCOLLECTION \((.*)\)', lines[index], re.M | re.I)
                    if patternMatch2:
                        print("Pattern 2: ", patternMatch2.group(1))
                    else:
                        print ("No Match !!!")
    fp.close()


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


def euclideanDistance(eachDM, prevCoorID, currCoorID):
    prevCoors = eachDM[prevCoorID].strip().split(' ')
    currCoors = eachDM[currCoorID].strip().split(' ')
    print (str(prevCoors) + " " + str(currCoors))
    #return math.sqrt((float(prevCoors[0]) - float(currCoors[0]))**2 + (float(prevCoors[1]) - float(currCoors[1]))**2)
    return funHaversine(float(currCoors[1]), float(currCoors[0]), float(prevCoors[1]), float(prevCoors[0]))


def getLocationsOfSourcesAndDataCenters(startIndex, endIndex):
    # create file for Sources. Though the source location are fixed, the spectrum bandwidth changes over time
    # Hence, it is important to save it as a file

    for srcID in range(startIndex, endIndex, 1):
        srcLocationX = random.randint(minX, maxX)
        srcLocationY = random.randint(minY, maxY)

        with open("Data/" + str(srcID) + ".txt", "w") as srcP:
            srcP.write("T X Y ")
            for s in range(S):
                srcP.write("S" + str(s) + " ")
            srcP.write("\n")

            for t in range(T):
                srcP.write(str(t) + " "  +str(srcLocationX) + " " + str(srcLocationY) + " ")

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
    for eachDM in DMTrajectories:
        dmID = dmID + 1
        currTime = 0
        currCoorID = 0
        nextCoorID = 1

        #dmSpeed = random.randint(VMIN, VMAX)
        dmSpeed = 50

        if dmID >= endIndex:
            break

        # print(str(dmID) + " " + str(startIndex) + " " + str(endIndex))
        tau = 2 #in minutes
        with open("Data2/"+str(dmID)+".txt", "w") as dmP:
            print ("For DM: " + str(dmID) + " Speed: " + str(dmSpeed))
            dmP.write("T X Y ");
            for s in range(S):
                dmP.write("S"+ str(s) + " ")
            dmP.write("\n")

            for t in range(currTime, T*60, tau):

                consumedTime = euclideanDistance(eachDM, currCoorID, nextCoorID)/dmSpeed
                # print("Curr " + str(currCoorID) + " Next " + str(nextCoorID) + " consTime: " + str(consumedTime))

                if consumedTime > t or t == T- tau:
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
                        currCoorID = 0
                    nextCoorID = currCoorID + 1

                # Change the bandwidth of each spectrum at each DSA node at each time epoch
                specBW = [random.randrange(minBW[s], maxBW[s]) for s in range(S)]
                # print ("Length of spectrum: " + str(S))
                for sBW in specBW:
                    dmP.write(str(sBW) + " ")
                dmP.write("\n")
        dmP.close()



#filepath = 'Data/trajectory.txt'

DMTrajectories = []         #stores the coordinates for each data mule

# Read trajectory for each data mule
readTrajectoryFile(DMTrajectories)

print("Length of DM trajectories: ", len(DMTrajectories))
# Randomly place sources (index from 0 to S -1)
# getLocationsOfSourcesAndDataCenters(0, NoOfSources)

# Randomly place DMs (index from (S - DM)
getLocationsOfDMs(DMTrajectories, NoOfSources, NoOfSources + NoOfDMs)

# Randomly place data centers (index from (DM -  DM + D))
# getLocationsOfSourcesAndDataCenters(NoOfSources + NoOfDMs, (NoOfSources + NoOfDMs + NoOfDataCenters ))
