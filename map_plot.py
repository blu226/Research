from gmplot import gmplot
import os
import numpy

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

def readFile(fileName, busName):
    currPath = []
    with open(fileName) as f:
        listOfLines = f.readlines()
        count = 0

        for line in listOfLines:
            lineStr = line.strip()
            lineStr = lineStr.split(" ")
            if count%2 == 0:
                currPath.append((float(lineStr[1]), float(lineStr[2])))
            count += 1
            # with open("UMASS/" + busName + ".txt", "a") as fw:
            #     newStr = lineStr[1] + " , " + lineStr[2]
            #     fw.write( newStr + "\n")
            #     count = count + 1
    # fw.close()
    f.close()
    return currPath


allPaths = []
#NOTE: RUN THIS ONE TIME
directory = "DieselNet-2007/gps_logs"
#generateData(directory)

folders = findfiles(directory)

# print (folders)
for ind in range(0, 1, 1):
    if folders[ind] is not ".DS_Store":
        print(folders[ind])

    folderPath = directory + "/" + str(folders[ind])
    currFiles = findfiles(folderPath)
    numOfFiles = len(currFiles)
    for fInd in range(0, numOfFiles):
        print(currFiles[fInd])
        filePath = folderPath + "/" + currFiles[fInd]
        currPath = readFile(filePath, folders[ind] + "_" + currFiles[fInd])
        allPaths.append(currPath)


# import pygmaps
# Place map
gmap = gmplot.GoogleMapPlotter(42.393658, -72.53295, 12)
# gmap = pygmaps.maps(42.340382, -72.496819, 15)

        # 0            1        2           3           4              5          6          7           8
        #Lime          Gold     Dark Red   Deep Pink  Forest Green    Blue       Black     Chocolate   Magneta
colors = ['#00FF00', '#FFD700', '#8B0000', '#FF1493', '#228B22',     '#0000FF', '#000000', '#D2691E', '#FF00FF', '#00008B', '#8B008B']
count = 0

for pInd in range(len(allPaths)):

    if pInd == 1 or pInd == 4 or pInd == 6 : #or pInd == 6 or pInd > 0
        print(str(pInd) + " " + str(len(allPaths[pInd])) + " " + str(allPaths[pInd]))
        path_lats, path_lons = zip(* allPaths[pInd])
        gmap.scatter(path_lats, path_lons, colors[pInd], size=60, marker=False)

# Marker
# hidden_gem_lat, hidden_gem_lon = 37.770776, -122.461689
# gmap.marker(hidden_gem_lat, hidden_gem_lon, 'cornflowerblue')

# Draw
gmap.draw("umass.html")