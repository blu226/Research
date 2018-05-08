from constants import *
from map_plot import *
import random
from computeHarvesine import *

def findDistance():
    with open("src_dst.txt", "r") as fp:
        lines = fp.readlines()
    fp.close()

    src = []
    dst = []
    for i in range(len(lines)):
        if i % 2 == 0:
            src.append(lines[i])
        else:
            dst.append(lines[i])

    for i in range(len(src)):
        line = src[i].split()

        for j in range(len(dst)):
            line2 = dst[j].split()
            print(funHaversine(float(line[1]),float(line[0]), float(line2[1]), float(line2[0])))
def getCoord():
    fileList = findfiles(lex_data_directory_day)
    fileList.sort()
    noOfFiles = len(fileList)

    lats = []
    longs = []

    for i in range(NoOfDMs):
        with open(lex_data_directory_day + str(i) + ".txt") as fp:
            lines = fp.readlines()
        fp.close()

        fileLen = len(lines)
        for j in range(2):
            rand = random.randint(0, fileLen - 1)

            line = lines[rand].strip()
            line = line.split()
            lats.append(line[2])
            longs.append(line[3])

    with open("src_dst.txt", "w") as fp:
        while(len(lats) > 8):
            fp.write(lats.pop() + " " + longs.pop() + "\n")



getCoord()

with open("src_dst.txt", "r") as fp:
    lines = fp.readlines()
fp.close()


for i in range(len(lines)):
    line = lines[i].strip()

    with open(lex_data_directory_day + str(i+NoOfDMs) + ".txt", "w") as fp:

        for j in range(StartTime, T + StartTime):
            fp.write(str(j) + "  00:00:00 " + line + "\t5\t15\t50\n")

#findDistance()