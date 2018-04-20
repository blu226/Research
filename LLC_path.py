import numpy
import math
import pickle
from constants import *



# Initialize the 5-D adjacency matrix where the value is 1 if
# node i and j are in communication range for a time period [ts, te] over any band s in the set S
# Assumption 1: Spectrum power and transmission range does not change
# Assumption 2: Only Spectrum bandwidth changes over time and location (i.e., at different nodes)
# Assumption 3: However given a bandwidth of a certain band at time t,
# it remains constant for the duration of transmission delay for any message
# Compute message colors (i.e., message transmission delays) for one spatial links and temporal links

# Compute message colors (i.e., message transmission delays) for spatial links (ONLY SPATIAL LINKS)
def computeADJ_T_2(specBW, LINK_EXISTS):
    ADJ_T = numpy.empty(shape=(V, V, T, len(M)))
    ADJ_T.fill(math.inf)

    ADJ_E = numpy.empty(shape=(V, V, T, len(M)))
    ADJ_E.fill(math.inf)

    Parent = numpy.empty(shape=(V, V, T, len(M)), dtype=int)
    Parent.fill(-1)

    Spectrum = numpy.empty(shape=(V, V, T, len(M)), dtype=int)
    Spectrum.fill(-1)

    # print ("M   i  j  s  ts  te :  Val  cT  LExi   BW    ")
    for m in range(len(M)):
        for t in range(T - tau, -1, -tau):
            for i in range(V):
                for j in range(V):

                    if i == j:
                        ADJ_T[i, j, t, m] = tau
                        ADJ_E[i, j, t, m] = epsilon
                        Spectrum[i, j, t, m] = 10
                        Parent[i, j, t, m] = i

                    else:
                        for s in S:
                            #bandwidth = 0 means there does not exist a link over that spectrum band
                            if specBW[i, j, s, t] > 0:
                                numerator = math.ceil(M[m] / specBW[i, j, s, t]) * (t_sd + idle_channel_prob * t_td)
                                consumedTime = tau * math.ceil(numerator/tau)

                                sensing_energy = math.ceil(M[m] / (specBW[i, j, s, t])) * t_sd * sensing_power
                                switching_energy = math.ceil(M[m] / (specBW[i, j, s, t])) * idle_channel_prob * switching_delay
                                transmission_energy = math.ceil(M[m]/specBW[i, j, s, t]) * idle_channel_prob * t_td * spectPower[s]

                                consumedEnergy = sensing_energy + switching_energy + transmission_energy
                                consumedEnergy = round(consumedEnergy, 2)

                                # print(i, j, t, consumedTime, m, specBW[i, j, s, t])
                                if (t + consumedTime) < T and ADJ_T[i, j, t, m] > consumedTime and LINK_EXISTS[
                                    i, j, s, t, (t + consumedTime)] < math.inf:
                                    ADJ_T[i, j, t, m] = consumedTime
                                    ADJ_E[i, j, t, m] = consumedEnergy
                                    Spectrum[i, j, t, m] = s + 1
                                    Parent[i, j, t, m] = i

                    if (t + tau) < T and ADJ_T[i, j, t, m] == math.inf and ADJ_T[i, j, (t + tau), m] != math.inf:
                        ADJ_T[i, j, t, m] = ADJ_T[i, j, (t + tau), m] + tau
                        ADJ_E[i, j, t, m] = ADJ_E[i, j, (t + tau), m] + epsilon
                        Parent[i, j, t, m] = Parent[i, j, t + tau, m]
                        Spectrum[i, j, t, m] = Spectrum[i, j, t + tau, m] + 10

    return ADJ_T, Parent, Spectrum, ADJ_E


# Determines the Least Latency Cost (LLC) Path for all messages in the STB graph
def LLC_PATH_ADJ_2(ADJ_T, ADJ_E, Parent, Spectrum, V, T, M):

    #print("k i j t : LLC Parent")
    for m in range(len(M)):
        for k in range(V):
            for i in range(V):
                for j in range(V):
                    for t in range(0, T, tau):
                        # leastTime = LLC_PATH[i, j, t, m]
                        #leastTime = math.inf

                        dcurr = ADJ_T[i, j, t, m]
                        d2 = math.inf
                        e2 = math.inf
                        # dalt = math.inf

                        d1 = ADJ_T[i, k, t, m]
                        e1 = ADJ_E[i, k, t, m]
                        if d1 < math.inf and (t + d1) < T:
                            d2 = ADJ_T[k, j, (t + int(d1)), m]
                            e2 = ADJ_E[k, j, (t + int(d1)), m]

                        if d1 + d2 < dcurr:
                            ADJ_T[i, j, t, m] = d1 + d2
                            ADJ_E[i, j, t, m]  = e1 + e2
                            Parent[i, j, t, m] = Parent[k, j, (t + int(d1)), m]
                            Spectrum[i, j, t, m] = Spectrum[k, j, (t + int(d1)), m]
                            # if i ==4 and j == 10 and t  == 0:
                            #     print(str(k) + " " + str(i) + " " + str(j) + " " + str(t) + " : " + str(
                            #                     ADJ_T[i, j, t, m]) + " " + str(Parent[i, j, t, m]))

    return ADJ_T, Parent, Spectrum, ADJ_E

def PRINT_LLC_PATH_FILE(LLC_PATH, ELC_PATH, Parent, Spectrum):
    m = 0

    file = open(path_to_folder + "LLC_PATH.txt", "w")
    file2 = open(path_to_folder + "LLC_PATH_Spectrum.txt", "w")
    file3 = open(path_to_folder + "LLC_Spectrum.txt", "w")

    file.write("#i\tj\tt\tm:\tPATH\n")
    file2.write("#i\tj\tt\tm:\tPATH\n")
    file3.write("#i\tj\tt\tm:\tPATH\n")

    # for t in range(0, T, tau):
        # for i in range(V):
        #     for j in range(V):
    i = 4
    j = 26
    t = 0

    # if i == j:
    #     continue
    # print("\n" + str(i) + " " + str(j) + " " + str(t) + " " + str(m) + " " + str(LLC_PATH[i, j, t, m]) + " : ", end=" ")
    # print("Path from " + str(u) + " -> "+ str(v) + " at time " + str(t) + " for message 0 is")

    if LLC_PATH[i, j, t, m] != math.inf:
        d = t + int(LLC_PATH[i, j, t, m])  # total delay

        print(i, j, t, d, LLC_PATH[i, j, t, m])

        path_str = str(j) + "\t"
        print_path_str = str(j) + "\t"
        spectrum_str = ""
        print("1. ", d, j)

        d = d - tau #this is important because of Spectrum[par_u, j, d, m]

        par_u = int(Parent[i, j, t, m])

        # temporal link
        while d > t and Spectrum[par_u, j, d, m] > 10:
            # Spectrum[par_u, j, d, m] -= 10
            print("2. ", d, par_u)
            spectrum_str += str(Spectrum[par_u, j, d, m]) + "\t"
            print_path_str += str(par_u) + " [" + str(Spectrum[par_u, j, d, m]) + ", " + str(d) + "]\t"
            path_str += str(par_u) + "\t"
            d = d - tau

        old_par_u = j
        while (par_u != -1 and par_u != i):
            print("3. ", d, par_u)
            spectrum_str += str(Spectrum[par_u, old_par_u, d, m]) + "\t"
            print_path_str += str(par_u) + " (" + str(Spectrum[par_u, old_par_u, d, m]) + ", " + str(d) + ")\t"
            path_str += str(par_u) + "\t"
            d = d - tau

            old_par_u = par_u
            par_u = int(Parent[i, par_u, d, m])

            # temporal link
            while d > t and Spectrum[par_u, old_par_u, d, m] > 10:
                # Spectrum[par_u, old_par_u, t, m] -= 10
                print("4. ", d, par_u)
                spectrum_str += str(Spectrum[par_u, old_par_u, d, m]) + "\t"
                print_path_str += str(par_u) + " [" + str(Spectrum[par_u, old_par_u, d, m]) + ", " + str(d) + "]\t"
                path_str += str(par_u) + "\t"
                d = d - tau



        spectrum_str +=  str(Spectrum[par_u, old_par_u, d, m]) + "\t"
        print_path_str += str(i) + " (" +  str(Spectrum[par_u, old_par_u, d, m]) + ", " + str(d) +")\t"
        path_str += str(i) + "\t"

        print("5. ", d, i)

        d = d - tau
        while d >= t and Spectrum[i, old_par_u, d, m] > 10:
            # Spectrum[par_u, old_par_u, t, m] -= 10
            print("6. ", d, i)
            spectrum_str += str(Spectrum[par_u, old_par_u, d, m]) + "\t"
            print_path_str += str(i) + " [" + str(Spectrum[i, old_par_u, d, m]) + ", " + str(
                d) + "]\t"
            path_str += str(i) + "\t"
            d = d - tau


        print (print_path_str, end = " ")
        file.write(str(i) + "\t" + str(j) + "\t" + str(t) + "\t" + str(M[m]) + "\t" + path_str + "\n")
        file2.write(str(i) + "\t" + str(j) + "\t" + str(t) + "\t" + str(M[m]) + "\t" +  str(ELC_PATH[i, j, t, m]) + "\t" + str(LLC_PATH[i, j, t, m]) + "\t:\t" + print_path_str + "\n")
        file3.write(str(i) + "\t" + str(j) + "\t" + str(t) + "\t" + str(M[m]) + "\t" + spectrum_str + "\n")

    file.close()
    file2.close()
    file3.close()

def PRINT_PATH_FILE_backup(LLC_PATH, Parent, Spectrum):

    file = open(path_to_folder + "path.txt", "w")

    i = 4
    j = 26
    t = 0
    m = 0
    # if i == 1 and j == 3:
    print("\n" + str(i) + " " + str(j) + " " + str(t) + " " + str(m) + " " + str(
        LLC_PATH[i, j, t, m]) + " : ", end=" ")
    # print("Path from " + str(u) + " -> "+ str(v) + " at time " + str(t) + " for message 0 is")
    if LLC_PATH[i, j, t, m] != math.inf:
        print_path_str = str(j) + " (" + str(Spectrum[i, j, t, m]) + ")  "
        par_u = int(Parent[i, j, t, m])

        path_str = str(j) + " "

        while par_u != -1 and t < T and par_u != i:
            path_str += str(par_u) + " "
            print_path_str += str(par_u) + " (" + str(Spectrum[i, par_u, t, m]) + ") "
            par_u = int(Parent[i, par_u, t, m])

        path_str += str(i) + " "
        print_path_str += str(i) + " "

        print("\nBackup: " , print_path_str, end=" ")
        file.write(str(i) + " " + str(j) + " " + str(t) + " " + str(M[m]) + " " + path_str + "\n")
    file.close()


def PRINT_LLC_PATH_FILE_3(LLC_PATH, ELC_PATH, Parent, Spectrum):


    file = open(path_to_folder + "LLC_PATH.txt", "w")
    file2 = open(path_to_folder + "LLC_PATH_Spectrum.txt", "w")
    file3 = open(path_to_folder + "LLC_Spectrum.txt", "w")

    file.write("#i\tj\tt\tm:\tPATH\n")
    file2.write("#i\tj\tt\tm:\tPATH\n")
    file3.write("#i\tj\tt\tm:\tPATH\n")

    m = 0

    # for m in range(len(M)):
    for t in range(0, T, tau):
        for i in range(V):
            for j in range(V):
                if i == j:
                    continue

                #0 9 0 ; 4 26 0; 1 4 0;
                if LLC_PATH[i, j, t, m] != math.inf:
                # if LLC_PATH[i, j, t, m] != math.inf and i == 4 and j == 26 and t == 0:
                    par_u = int(Parent[i, j, t, m])

                    print_path_str = str(j) + " (" + str(Spectrum[i, j, t, m]) + ")\t"
                    path_str = str(j) + "\t"
                    spec_str = str(Spectrum[i, j, t, m]) + "\t"

                    temp_spec_val = Spectrum[i, j, t, m]

                    while temp_spec_val > 10:
                        temp_spec_val -= 10
                        path_str += str(par_u) + "\t"
                        spec_str += str(temp_spec_val) + "\t"
                        print_path_str += str(par_u) + " (" + str(temp_spec_val) + ")  "

                    while par_u != -1 and t < T and par_u != i:
                        path_str += str(par_u) + "\t"
                        print_path_str += str(par_u) + " (" + str(Spectrum[i, par_u, t, m]) + ")\t"
                        spec_str += str(Spectrum[i, par_u, t, m]) + "\t"

                        #Get the value earlier than updating par_u
                        temp_spec_val = Spectrum[i, par_u, t, m]

                        par_u = int(Parent[i, par_u, t, m])

                        while temp_spec_val > 10:
                            temp_spec_val -= 10
                            path_str += str(par_u) + "\t"
                            spec_str += str(temp_spec_val) + "\t"
                            print_path_str += str(par_u) + " (" + str(temp_spec_val) + ")\t"


                    path_str += str(i)
                    print_path_str += str(i) +"\t"


                    # if i == 1 and j == 4 and t == 0:
                    print("\nPath " , print_path_str + " LLC: " , LLC_PATH[i, j, t, m], end=" ")

                    file.write(str(i) + "\t" + str(j) + "\t" + str(t) + "\t" + str(M[m]) + "\t" + path_str + "\n")
                    file2.write(
                        str(i) + "\t" + str(j) + "\t" + str(t) + "\t" + str(M[m]) + "\t" + str(ELC_PATH[i, j, t, m]) + "\t" + str(
                            LLC_PATH[i, j, t, m]) + "\t:\t" + print_path_str + "\n")
                    file3.write(str(i) + "\t" + str(j) + "\t" + str(t) + "\t" + str(M[m]) + "\t" + spec_str + "\n")

    file.close()
    file2.close()
    file3.close()

