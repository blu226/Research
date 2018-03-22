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

        for line in listOfLines:
            lineStr = line.strip()
            lineStr = lineStr.split(" ")
            currPath.append((float(lineStr[1]), float(lineStr[2])))

            # with open("UMASS/" + busName + ".txt", "a") as fw:
            #     newStr = lineStr[1] + " , " + lineStr[2]
            #     fw.write( newStr + "\n")
            #     count = count + 1
    # fw.close()
    f.close()
    return currPath


allPaths = []
#NOTE: RUN THIS ONE TIME
directory = "/Users/vijay/Dropbox/MobilityTraces/DieselNet-2007/gps_logs"
#generateData(directory)

folders = findfiles(directory)

# print (folders)
for ind in range(0, 1, 1):
    if folders[ind] is not ".DS_Store":
        print(folders[ind])

    folderPath = directory + "/" + str(folders[ind])
    currFiles = findfiles(folderPath)

    for fInd in range(0, 5):
        print(currFiles[fInd])
        filePath = folderPath + "/" + currFiles[fInd]
        currPath = readFile(filePath, folders[ind] + "_" + currFiles[fInd])
        allPaths.append(currPath)


# import pygmaps
# Place map
gmap = gmplot.GoogleMapPlotter(42.393658, -72.53295, 12)
# gmap = pygmaps.maps(42.340382, -72.496819, 15)

colors = ['#FFD700', '#00FF00', '#8B0000', '#FF1493', '#228B22']
count = 0
for pInd in range(len(allPaths)):

    # Polygon
    # path = [
    #     (37.771269, -122.511015),
    #     (42.28021, - 72.403496),
    #     (42.281666, - 72.40445),
    #     (42.28291, - 72.40526),
    #     (42.284184, - 72.40615),
    #     (42.285515, - 72.406784),
    #     ]
    # if pInd == 0:
    #     continue

    if pInd == 0 or pInd == 3:
        print(allPaths[pInd])
        golden_gate_park_lats, golden_gate_park_lons = zip(* allPaths[pInd])
        gmap.scatter(golden_gate_park_lats, golden_gate_park_lons, colors[pInd], size=40, marker=True)

    count = count + 1

# Marker
# hidden_gem_lat, hidden_gem_lon = 37.770776, -122.461689
# gmap.marker(hidden_gem_lat, hidden_gem_lon, 'cornflowerblue')

# Draw
gmap.draw("umass.html")