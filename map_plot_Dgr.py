from gmplot import gmplot
import os
import numpy
import random
import math

def getPath():
    pathToFolder = "DieselNet-2007/gps_logs"


def findfiles(directory):
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

def readFile(fileName):
    currPath = []
    with open(fileName) as f:
        listOfLines = f.readlines()
        count = 0

        for line in listOfLines:
            lineStr = line.strip()
            lineStr = lineStr.split(",")
            # if count%2 == 0:
            # print(lineStr[3])
            if '#' in lineStr[0]:
                continue
            else:
                currPath.append((float(lineStr[0]), float(lineStr[1])))

            count += 1
            # with open("UMASS/" + busName + ".txt", "a") as fw:
            #     newStr = lineStr[1] + " , " + lineStr[2]
            #     fw.write( newStr + "\n")
            #     count = count + 1
    # fw.close()
    f.close()
    return currPath


allPaths = []
allFiles = []
#NOTE: RUN THIS ONE TIME
directory = "CityMapData/Durgapur"
#generateData(directory)

folders = findfiles(directory)
folders.sort()
foldersLen = len(folders)
foldersLen = 24

#print ("Folder is: " + folders)
for ind in range(23, foldersLen, 1):
    # print("Current Folder " + folders[ind])

    if ".DS_Store" not in folders and 'DATA' not in str(folders[ind]):
        print("Current Folder " + folders[ind])
    else:
        folderPath = directory + "/" + str(folders[ind])
        currFiles = findfiles(folderPath)
        currFiles.sort()

        numOfFiles = len(currFiles)
        for fInd in range(0, numOfFiles):
            if "GPS" in currFiles[fInd]:
                # print("Current File " + currFiles[fInd])
                filePath = folderPath + "/" + currFiles[fInd]
                currPath = readFile(filePath)
                allFiles.append(filePath)
                allPaths.append(currPath)


        # import pygmaps
        # Place map
        gmap = gmplot.GoogleMapPlotter(23.52818659, 87.3111636, 12)
        # gmap = pygmaps.maps(42.340382, -72.496819, 15)

                # 0            1        2           3           4              5          6          7           8
                #Lime          Gold     Dark Red   Deep Pink  Forest Green    Blue       Black     Chocolate   Magneta
        colors = ['#00FF00', '#FFD700', '#8B0000', '#FF1493', '#228B22',     '#0000FF', '#000000', '#D2691E', '#FF00FF', '#00008B', '#8B008B']
        count = 0

        for pInd in range(len(allPaths)):

            if pInd == 1 or pInd == 2 or pInd == 3 : #or pInd == 6 or pInd > 0
                print("\n" + allFiles[pInd])
                print(str(pInd) + " " + str(len(allPaths[pInd])) + " " + str(allPaths[pInd]))
                path_lats, path_lons = zip(* allPaths[pInd])
                colorInd = int(pInd%8)
                # print ("index: ", colorInd)
                gmap.scatter(path_lats, path_lons, colors[colorInd], size=60, marker=False)

                # Draw
                gmap.draw(allFiles[pInd].split("/")[2] + str(ind  + 1) + ".html")