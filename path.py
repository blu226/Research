import numpy
import math
from STB_help import *
from constants import *


# Compute message colors (i.e., message transmission delays) for spatial links (ONLY SPATIAL LINKS)
def computeADJ_T_2(specBW, LINK_EXISTS, V, S, T, M, tau):
    ADJ_T = numpy.empty(shape=(V, V, S, T, len(M)))
    ADJ_T.fill(math.inf)

    Parent = numpy.empty(shape=(V, V, T, len(M)))
    Parent.fill(-1)

    # print ("M   i  j  s  ts  te :  Val  cT  LExi   BW    ")
    for m in range(len(M)):
        for t in range(T - tau, -1, -tau):
            for i in range(V):
                for j in range(V):
                    for s in range(S):

                        consumedTime = tau * math.ceil(M[m] / (tau * specBW[i, j, s, t]))

                        if i == j:
                            consumedTime = tau

                        if (t + consumedTime < T) and LINK_EXISTS[i, j, s, t, (t + consumedTime)] < math.inf:

                            # print(str(i) + " " + str(j) + " "  + str(s) + " " + str(t) + " " + str(t+consumedTime) + " " + str(LINK_EXISTS[ i, j, s, t, (t + consumedTime)]));
                            ADJ_T[i, j, s, t, m] = consumedTime
                            Parent[i, j, t, m] = i

                        elif (t + tau) < T and ADJ_T[i, j, s, (t + tau), m] != math.inf:
                            ADJ_T[i, j, s, t, m] = ADJ_T[i, j, s, (t + tau), m] + tau
                            Parent[i, j, t, m] = Parent[i, j, t + tau, m]

                        # else:
                        #     ADJ_T[i, j, s, t, m] = math.inf
                        #     Parent[i, j, t, m] = -1

                            # if t + consumedTime < T and ADJ_T[i, j, s, t, m] != math.inf and ADJ_T[i, j, s, t, m] > 1:
                            #     print(str(M[m]) + "  " + str(i) + "  " + str(j) + "  " + str(s) + "  " + str(
                            #         t) + "   " + str(t + consumedTime) + "  :  " + str(
                            #         ADJ_T[i, j, s, t, m]) + "  " + str(
                            #         consumedTime) + "   " + str(LINK_EXISTS[i, j, s, t, (t + consumedTime)]) + "   " + str(
                            #         specBW[i, j, s, t]))

    return ADJ_T, Parent


# Determines the Least Latency Cost (LLC) Path for all messages in the STB graph
def LLC_PATH_ADJ_2(ADJ_T, Parent, V, S, T, M, tau):
    # LLC = Least Latency Cost Path
    LLC_PATH = numpy.empty(shape=(V, V, T, len(M)))
    LLC_PATH.fill(math.inf)

    Spectrum = numpy.empty(shape=(V, V, T, len(M)))
    Spectrum.fill(-1)

    print("k i j t : LLC Parent")
    for m in range(len(M)):
        for t in range(T - tau, -1, -tau):
            for k in range(V):
                for i in range(V):
                    for j in range(V):

                        # leastTime = LLC_PATH[i, j, t, m]
                        leastTime = math.inf
                        for s1 in range(S):
                            for s2 in range(S):
                                for s3 in range(S):

                                    dcurr = ADJ_T[i, j, s1, t, m]
                                    d2 = math.inf
                                    # dalt = math.inf

                                    d1 = ADJ_T[i, k, s2, t, m]
                                    if d1 < math.inf and (t + d1) < T:
                                        d2 = ADJ_T[k, j, s3, (t + int(d1)), m]

                                    dalt = d1 + d2
                                    # print ("D: " + str(dcurr) +" d1: " + str(d1) + " d2: " + str(d2))

                                    if dalt <= dcurr and dalt < leastTime and dalt < LLC_PATH[i, j, t, m]:
                                        leastTime = dalt
                                        LLC_PATH[i, j, t, m] = dalt
                                        Spectrum[i, k, t, m] = s2
                                        Spectrum[k, j, (t + int(d1)), m] = s3
                                        Parent[i, j, t, m] = Parent[k, j, (t + int(d1)), m]

                                    elif dcurr < dalt and dcurr < leastTime and dcurr < LLC_PATH[i, j, t, m]:
                                        leastTime = dcurr
                                        LLC_PATH[i, j, t, m] = leastTime
                                        # Parent[i, j, t, m] = i
                                        Spectrum[i, j, t, m] = s1
                        if i == j:
                            Spectrum[i, j, t, m] = -1
                                    # print(str(k) + " " + str(i) + " " + str(j) + " " + str(t) +  " : " + str(LLC_PATH[i, j, t, m]) + " " + str(Parent[i, j, t, m]))
                                    # if i == 0 and j == 2 and t == 0 and m == 0:

                                    # print("i: " + str(i) + " j: " + str(j) + " k: " + str(k) + " s1: " + str(
                                    #     s1) + " s2: " + str(s2) + " s3: " + str(s3) + " t: " + str(t) + " m: " + str(m))
                                    # print ("D: " + str(dcurr) +" d1: " + str(d1) + " d2: " + str(d2) + " " + str(LLC_PATH[i,j,t,m]) + "\n")

                                        # if i == 0 and j == 3 and k == 1 and t == 0:
                                        # print("Value here: " + str(LLC_PATH[0, 3, 0, 0]))
    # print("Value here: " + str(LLC_PATH[0,3,0,0]))

    return LLC_PATH, Parent, Spectrum

def PRINT_PATH_2(Parent, Spectrum):
    V = NoOfDMs
    m = 0
    tau = 1

    print("i j t m: PATH")
    for t in range(T):
        for i in range(V):
            for j in range(V):
                print(str(i) + " " + str(j) + " " + str(t) + " " + str(M[0]) + ": ", end=" ")
                # print("Path from " + str(u) + " -> "+ str(v) + " at time " + str(t) + " for message 0 is")
                print(str(i) + " - ", end=' ')
                print_path_util(Parent, i, j, t, 0)
                print(j)

def print_path_util(Parent, src, dst, t, m):
    if int(Parent[src, dst, t, m]) == src or Parent[src, dst, t, m] == -1:
        return

    print_path_util(Parent, src, int(Parent[src, dst, t, m]), t + 1, m)
    print(str(int(Parent[src, dst, t, m])) + " - ", end=' ')
