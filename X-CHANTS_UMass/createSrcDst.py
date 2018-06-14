from constants import *
from STB_help import *
import random
from computeHarvesine import *

def findDistance():
    with open("srcdst.txt", "r") as fp:
        lines = fp.readlines()
    fp.close()

    src = []
    dst = []
    for i in range(len(lines)):
        # if i % 2 == 0:
        src.append(lines[i])
        # else:
        #     dst.append(lines[i])

    for i in range(len(src)):
        line = src[i].split()

        for j in range(len(src)):
            line2 = src[j].split()
            print(funHaversine(float(line[1]),float(line[0]), float(line2[1]), float(line2[0])) / 1000)
def getCoord():
    fileList = findfiles(lex_data_directory_day)
    fileList.sort()
    noOfFiles = len(fileList)

    lats = []
    longs = []

    for i in range(NoOfDMs):
        with open(lex_data_directory_day + str(i) + ".txt") as fp:
            lines = fp.readlines()
            #print(fp)
        fp.close()

        fileLen = len(lines)
        for j in range(2):
            rand = random.randint(0, fileLen - 1)

            line = lines[rand].strip()
            line = line.split()
            while line[2] == '-' or line[2] == '0.0':
                rand = random.randint(0, fileLen - 1)
                line = lines[rand].strip()
                line = line.split()

            lats.append(line[2])
            longs.append(line[3])


    with open("src_dst.txt", "w") as fp:
        while(len(lats) > 8):
            fp.write(lats.pop() + " " + longs.pop() + "\n")



#getCoord()
def getSrcDst(time, day):
    with open("srcdst.txt", "r") as fp:
        lines = fp.readlines()
    fp.close()

    StartTime = time

    for day_num in ["1","2"]:

        for i in range(len(lines)):
            line = lines[i].strip()

            with open("../DataMules/" + day + "Day" + day_num + "/" + str(i) + ".txt", "w") as fp:

                for j in range(StartTime, T + StartTime + 1):
                    fp.write(str(j) + "  00:00:00 " + line + "\t5\t15\t50\n")

# findDistance()

# directorys = ['2007-10-23_2007-10-24/', '2007-10-24_2007-10-25/', '2007-10-25_2007-10-26/', '2007-10-26_2007-10-27/','2007-10-29_2007-10-30/','2007-10-30_2007-10-31/','2007-10-31_2007-11-01/','2007-11-01_2007-11-02/','2007-11-02_2007-11-03/','2007-11-03_2007-11-04/','2007-11-04_2007-11-05/','2007-11-05_2007-11-06/','2007-11-06_2007-11-07/','2007-11-07_2007-11-08/','2007-11-09_2007-11-10/','2007-11-10_2007-11-11/']
# # startTime = [400,950,850,500,950,650,950,400,400,900,950,600,900,850,400,900,950,950]
# directorys = ['2007-11-07_2007-11-08/']
# startTime = [500]

# directorys = ['2007-10-23_2007-10-24/', '2007-10-24_2007-10-25/', '2007-10-25_2007-10-26/', '2007-10-26_2007-10-27/','2007-10-29_2007-10-30/','2007-10-30_2007-10-31/','2007-10-31_2007-11-01/','2007-11-01_2007-11-02/','2007-11-02_2007-11-03/','2007-11-03_2007-11-04/','2007-11-04_2007-11-05/','2007-11-05_2007-11-06/','2007-11-06_2007-11-07/','2007-11-07_2007-11-08/','2007-11-09_2007-11-10/','2007-11-10_2007-11-11/']
# startTime = [800,800,680,920,680,920,680,920,680,560,800,560,680,560,800,560,800,560]
directorys = ['2007-11-06_2007-11-07/']
startTime = [560]
for i in range(len(directorys)):
    # getSrcDst(startTime[i],directorys[i])
    findDistance()