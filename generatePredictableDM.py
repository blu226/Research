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


def createLinkFunction(DMTrajectories, DMSpeed, minBW, maxBW, T):
    dmID = -1
    S = len(minBW)

    for eachDM in DMTrajectories:
        dmID = dmID + 1
        currTime = 0
        currCoorID = 0
        nextCoorID = 1

        with open("Data/"+str(dmID)+".txt", "w") as dmP:
            print ("For DM: " + str(dmID) + " Speed: " + str(DMSpeed[dmID]))
            dmP.write("T X Y ");
            for s in range(S):
                dmP.write("S"+ str(s) + " ")
            dmP.write("\n")

            for t in range(currTime, T):

                consumedTime = euclideanDistance(eachDM, currCoorID, nextCoorID)/DMSpeed[dmID]
                # print("Curr " + str(currCoorID) + " Next " + str(nextCoorID) + " consTime: " + str(consumedTime))

                if consumedTime > t or t == T-1:
                    # write to the file
                    # print (str(t) + " " + str(eachDM[currCoorID]))
                    dmP.write(str(t) + " " + eachDM[currCoorID].strip() + " ")

                else:
                    # print(str(t) + " " + str(eachDM[nextCoorID]))
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

# Generate a random yet unique speed for each data mule
DMSpeed = [random.randint(VMIN, VMAX) for i in range(len(DMTrajectories))]

# Calculate the position for each data mule at each time epoch
# Here, the duration of each time epoch is 1 unit
createLinkFunction(DMTrajectories, DMSpeed, minBW, maxBW, T)