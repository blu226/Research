import re
import random
import math

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

def createLinkFunction(DMTrajectories, DMSpeed, T):
    dmID = -1

    for eachDM in DMTrajectories:
        dmID = dmID + 1
        currTime = 0
        currCoorID = 0
        nextCoorID = 1
        with open("Data/"+str(dmID)+".txt", "w") as dmP:
            print ("For DM: " + str(dmID) + " Speed: " + str(DMSpeed[dmID]))
            for t in range(currTime, T):

                consumedTime = euclideanDistance(eachDM, currCoorID, nextCoorID)/DMSpeed[dmID]
                # print("Curr " + str(currCoorID) + " Next " + str(nextCoorID) + " consTime: " + str(consumedTime))


                if consumedTime > t or t == T-1:
                    # write to the file
                    # print (str(t) + " " + str(eachDM[currCoorID]))
                    dmP.write(str(t) + " " + str(eachDM[currCoorID]) + "\n")

                else:
                    # print(str(t) + " " + str(eachDM[nextCoorID]))
                    dmP.write(str(t) + " " + str(eachDM[nextCoorID]) + "\n")
                    currCoorID = nextCoorID
                    if currCoorID == len(eachDM) - 1:
                        currCoorID = 0
                    nextCoorID = currCoorID + 1

        dmP.close()



filepath = 'Data/trajectory.txt'

NoOfDMs = 2
DMTrajectories = []         #stores the coordinates for each data mule
VMIN = 1
VMAX = 10
T = 51
specRange = [10, 50, 100]  #ISM, LTE, TV

readTrajectoryFile(filepath, DMTrajectories)
DMSpeed = [random.randint(VMIN, VMAX) for i in range(len(DMTrajectories))]

#print (DMTrajectories)
createLinkFunction(DMTrajectories, DMSpeed, T)