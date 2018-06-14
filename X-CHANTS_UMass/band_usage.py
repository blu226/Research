import os



directory = "../Bands_UMass/2007-11-06_2007-11-07/Day1/ALL/XChants/11/"
# folders = os.listdir(directory)
# folders.sort()

# for i in range(0, len(folders) - 10):
#
#     bands = ["/ALL", "/CBRS", "/LTE","/TV", "/ISM" ]
#     file = folders[i]
#     print(file)
#
#     for band in bands:
#         print(band)
path = directory + "/LLC_Spectrum.txt"

ISM = 0
TV = 0
CBRS = 0
LTE = 0
temporal = 0

with open(path,"r") as f:
    lines = f.readlines()[1:]

for line in lines:
    line_arr = line.strip().split()

    for i in range(4, len(line_arr)):
        spec = int(line_arr[i])

        if spec == 1:
            TV += 1

        elif spec == 2:
            ISM += 1

        elif spec == 3:
            LTE += 1

        elif spec == 4:
            CBRS += 1

        else:
            temporal += 1

total = TV + ISM + LTE + CBRS + temporal


print("TV: ", TV/total)
print("ISM: ", ISM/total)
print("LTE: ", LTE/total)
print("CBRS: ", CBRS/total)
print("Temporal Links: ",temporal/total, "\n")


