import pickle
import math

from STB_help import *
from constants import *

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
LINK_EXISTS.fill(math.inf)

if not os.path.exists(lex_data_directory):
    os.makedirs(lex_data_directory)

createLinkExistenceADJ("Lexington")

if not os.path.exists(path_to_folder):
    os.makedirs(path_to_folder)

LE_file = open( path_to_folder + "LINK_EXISTS.pkl", 'wb')
pickle.dump(LINK_EXISTS, LE_file)
LE_file.close()

print("Size of Link Exists: " + str(len(LINK_EXISTS)) + " " + str(len(LINK_EXISTS[0])) + " " + str(len(LINK_EXISTS[0][0])) + " " + str(len(LINK_EXISTS[0][0][0])))
save_in_file("LINK_EXISTS.txt", LINK_EXISTS)
#printMAT(LINK_EXISTS)