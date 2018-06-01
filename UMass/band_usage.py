import os



directory = "../Bands/"
folders = os.listdir(directory)
folders.sort()

for file in folders:
    path = directory + file + "/LLC_Spectrum.txt"

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

            if spec == 0:
                TV += 1

            elif spec == 1:
                ISM += 1

            elif spec == 2:
                LTE += 1

            elif spec == 3:
                CBRS += 1

            else:
                temporal += 1

    total = TV + ISM + LTE + CBRS + temporal

    print(file)
    print("TV: ", TV/total)
    print("ISM: ", ISM/total)
    print("LTE: ", LTE/total)
    print("CBRS: ", CBRS/total)
    print("Temporal Links: ",temporal/total, "\n")


