import os
from STB_help import *

output_file = open("Lex_RTT.txt", 'w')

all_files = os.listdir("./")

for aFile in all_files:
    if "Lexington" in aFile:

        Lex_dir = aFile + '/'
        rounds = findDir(Lex_dir)

        for round in rounds:

            days = findDir(Lex_dir + round + '/')
            for day in days:

                if len(day.split('_')) == 1:
                    dataMule_path = Lex_dir + round + '/' + day + '/'
                    output_file.write("______________________________________\n")
                    output_file.write(dataMule_path + '\n')
                    print(dataMule_path)

                    bus_files = findfiles(dataMule_path)
                    bus_files.sort()

                    for file in bus_files:

                        file_name_arr = file.split('.')
                        file_num = int(file_name_arr[0])

                        if file_num > 11:

                            with open(dataMule_path + file, 'r') as f:
                                lines = f.readlines()[1:]

                            start_line = lines[0].strip().split()
                            startX = start_line[1]
                            startY = start_line[2]

                            times_at_start = []

                            for time in range(10, len(lines)):
                                line = lines[time].strip().split()
                                time = line[0]
                                x = line[1]
                                y = line[2]

                                if startX == x and startY == y:
                                    times_at_start.append(time)

                            print("bus", file_num, " RTT =", times_at_start[0])
                            output_file.write("bus " + str(file_num) + "  RTT = " + str(times_at_start[0]) + '\n')

            output_file.write("\n")