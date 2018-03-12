import re
import random
import math
from constants import *

def readTrajectoryFile(filepath, DMTrajectories):
    with open(filepath) as fp:
        lines = fp.readlines()

        for index in range(0, len(lines)):
            patternMatch = re.match(r'^LINESTRING\((.*)\)', lines[index], re.M | re.I)

            if patternMatch:
                # print ("patternMatch.group(1) : ", patternMatch.group(1))
                trajectoryCoord = patternMatch.group(1)
                DMTrajectories.append(trajectoryCoord.strip().split(','))

            else:
                print ("No Match !!!")
    fp.close()

def euclideanDistance(eachDM, prevCoorID, currCoorID):
    prevCoors = eachDM[prevCoorID].strip().split(' ')
    currCoors = eachDM[currCoorID].strip().split(' ')
    # print (str(prevCoors) + " " + str(currCoors))
    return math.sqrt((float(prevCoors[0]) - float(currCoors[0]))**2 + (float(prevCoors[1]) - float(currCoors[1]))**2)

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

        dmSpeed = random.randint(VMIN, VMAX)

        if dmID >= endIndex:
            break

        # print(str(dmID) + " " + str(startIndex) + " " + str(endIndex))

        with open("Data/"+str(dmID)+".txt", "w") as dmP:
            print ("For DM: " + str(dmID) + " Speed: " + str(dmSpeed))
            dmP.write("T X Y ");
            for s in range(S):
                dmP.write("S"+ str(s) + " ")
            dmP.write("\n")

            for t in range(currTime, T):

                consumedTime = euclideanDistance(eachDM, currCoorID, nextCoorID)/dmSpeed
                # print("Curr " + str(currCoorID) + " Next " + str(nextCoorID) + " consTime: " + str(consumedTime))

                if consumedTime > t or t == T-1:
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



filepath = 'Data/trajectory.txt'

DMTrajectories = []         #stores the coordinates for each data mule

# Read trajectory for each data mule
readTrajectoryFile(filepath, DMTrajectories)

# Randomly place sources (index from 0 to S -1)
getLocationsOfSourcesAndDataCenters(0, NoOfSources)

# Randomly place DMs (index from (S - DM)
getLocationsOfDMs(DMTrajectories, NoOfSources, NoOfSources + NoOfDMs)

# Randomly place data centers (index from (DM -  DM + D))
getLocationsOfSourcesAndDataCenters(NoOfSources + NoOfDMs, (NoOfSources + NoOfDMs + NoOfDataCenters ))
