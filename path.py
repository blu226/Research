import numpy
import math
from STB_help import *
from constants import *

# Compute message colors (i.e., message transmission delays) for spatial links (ONLY SPATIAL LINKS)
def computeADJ_T_2(specBW, LINK_EXISTS):
    ADJ_T = numpy.empty(shape=(V, V, T, len(M)))
    ADJ_T.fill(math.inf)

    ADJ_E = numpy.empty(shape=(V, V, T, len(M)))
    ADJ_E.fill(math.inf)

    Parent = numpy.empty(shape=(V, V, T, len(M)))
    Parent.fill(-1)

    Spectrum = numpy.empty(shape=(V, V, T, len(M)))
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
                        leastConsumedTime = math.inf
                        for s in range(S):
                            consumedTime = tau * math.ceil(M[m] / (tau * specBW[i, j, s, t]))
                            consumedEnergy = (M[m] / (specBW[i, j, s, t])) * spectPower[s]
                            consumedEnergy = round(consumedEnergy, 2)

                            if t + consumedTime < T and ADJ_T[i, j, t, m] > consumedTime and LINK_EXISTS[
                                i, j, s, t, (t + consumedTime)] < math.inf:
                                ADJ_T[i, j, t, m] = consumedTime
                                ADJ_E[i, j, t, m] = consumedEnergy
                                Spectrum[i, j, t, m] = s + 1
                                Parent[i, j, t, m] = i


                    # if (t + leastConsumedTime < T):
                    #
                    #     # print(str(i) + " " + str(j) + " "  + str(s) + " " + str(t) + " " + str(t+consumedTime) + " " + str(LINK_EXISTS[ i, j, s, t, (t + consumedTime)]));
                    #     ADJ_T[i, j, t, m] = leastConsumedTime
                    #     Parent[i, j, t, m] = i

                    if (t + tau) < T and ADJ_T[i, j, t, m] == math.inf and ADJ_T[i, j, (t + tau), m] != math.inf:
                        ADJ_T[i, j, t, m] = ADJ_T[i, j, (t + tau), m] + tau
                        ADJ_E[i, j, t, m] = ADJ_E[i, j, (t + tau), m] + epsilon
                        Parent[i, j, t, m] = Parent[i, j, t + tau, m]
                        Spectrum[i, j, t, m] = Spectrum[i, j, t + tau, m] + 10
                        #Spectrum[i, j, t, m] = 10

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
                            # if i ==0 and j == 2 and t  == 0:
                            #     print(str(k) + " " + str(i) + " " + str(j) + " " + str(t) + " : " + str(
                            #                     ADJ_T[i, j, t, m]) + " " + str(Parent[i, j, t, m]))

    return ADJ_T, Parent, Spectrum, ADJ_E

def PRINT_LLC_PATH_FILE(LLC_PATH, ELC_PATH, Parent, Spectrum):
    m = 0

    file = open(path_to_folder + "LLC_PATH.txt", "w")
    file2 = open(path_to_folder + "LLC_PATH_Spectrum.txt", "w")
    #print("i j t m: PATH")
    for t in range(0, T, tau):
        for i in range(V):
            for j in range(V):

                # print("\n" + str(i) + " " + str(j) + " " + str(t) + " " + str(m) + " " + str(LLC_PATH[i, j, t, m]) + " : ", end=" ")
                # print("Path from " + str(u) + " -> "+ str(v) + " at time " + str(t) + " for message 0 is")

                if LLC_PATH[i, j, t, m] != math.inf:
                    d = t + int(LLC_PATH[i, j, t, m])  # total delay

                if LLC_PATH[i, j, t, m] != math.inf: #path exists
                    par_u = int(Parent[i, j, t, m])

                    path_str = str(j) + " "
                    print_path_str = str(j) + " "

                    d = d - tau

                    # temporal link
                    while d > t and Spectrum[par_u, j, d, m] > 10:
                        # Spectrum[par_u, j, d, m] -= 10
                        print_path_str += str(par_u) + " [" + str(Spectrum[par_u, j, d, m]) + ", " + str(d) + "] "
                        path_str += str(par_u) + " "
                        d = d - tau

                    old_par_u = j
                    while (par_u != -1 and par_u != i):

                        path_str += str(par_u) + " "
                        print_path_str += str(par_u) + " (" + str(Spectrum[par_u, old_par_u, d, m]) + ", " + str(d) + ") "

                        d = d - tau

                        # temporal link
                        while d > t and Spectrum[par_u, old_par_u, d, m] > 10:
                            # Spectrum[par_u, old_par_u, t, m] -= 10
                            print_path_str += str(par_u) + " [" + str(Spectrum[par_u, old_par_u, d, m]) + ", " + str(d) + "] "
                            path_str += str(par_u) + " "
                            d = d - tau

                        old_par_u = par_u
                        par_u = int(Parent[i, par_u, t, m])

                    path_str += str(i) + " "
                    print_path_str += str(i) + " (" +  str(Spectrum[par_u, old_par_u, d, m]) + ", " + str(d) +") "

                    d = d - tau
                    while d >= t and Spectrum[i, old_par_u, d, m] > 10:
                        # Spectrum[par_u, old_par_u, t, m] -= 10
                        print_path_str += str(i) + " [" + str(Spectrum[i, old_par_u, d, m]) + ", " + str(
                            d) + "] "
                        path_str += str(i) + " "
                        d = d - tau

                    # print (print_path_str, end = " ")
                    file.write(str(i) + " " + str(j) + " " + str(t) + " " + str(M[m]) + " " + path_str + "\n")
                    file2.write(str(i) + " " + str(j) + " " + str(t) + " " + str(M[m]) + " " +  str(ELC_PATH[i, j, t, m]) + " " + str(LLC_PATH[i, j, t, m])  + " : " + print_path_str + "\n")
    file.close()
    file2.close()


    def PRINT_PATH_FILE_backup(LLC_PATH, Parent, Spectrum):
        V = NoOfDMs
        m = 0
        tau = 1

        file = open("path.txt", "w")
        # print("i j t m: PATH")
        for t in range(0, T, tau):
            for i in range(V):
                for j in range(V):
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

                        print(print_path_str, end=" ")
                        file.write(str(i) + " " + str(j) + " " + str(t) + " " + str(M[m]) + " " + path_str + "\n")
        file.close()
