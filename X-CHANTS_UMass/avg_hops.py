import os
import numpy as np



directory = "Bands/"
folders = os.listdir(directory)
folders.sort()

for i in range(0, 1):
    hops = []
    bands = ["/ALL", "/CBRS", "/LTE","/TV", "/ISM" ]
    file = folders[i]
    print(file)

    for band in bands:
        print(band)
        path = directory + file + band + "/LLC_PATH.txt"

        with open(path, "r") as f:
            lines = f.readlines()[1:]

        num_lines = len(lines)
        total_hops = 0
        max = 0
        min = 100000

        for line in lines:
            line_arr = line.strip().split()
            line_arr = set(line_arr[4:])
            line_arr = list(line_arr)

            num_hops = len(line_arr)

            if num_hops < min:
                min = num_hops

            if num_hops > max:
                max = num_hops

            hops.append(num_hops)


        print("Average: ", np.mean(hops))
        print("Std: ", np.std(hops))
        print("Median: ", np.median(hops))
        print("Max: ", max)
        print("Min: ", min, "\n")

        for i in range(min,max):
            num = hops.count(i)
            length = len(hops)
            ratio = num / length
            print(str(i) + ": " + str(ratio) )