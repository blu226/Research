import numpy
import math
from STB_help import *
from constants import *

# Compute message colors (i.e., message transmission delays) for spatial links (ONLY SPATIAL LINKS)
def computeADJ_T_2(specBW, LINK_EXISTS, tau):
    ADJ_T = numpy.empty(shape=(V, V, T, len(M)))
    ADJ_T.fill(math.inf)

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
                        Spectrum[i, j, t, m] = 10
                        Parent[i, j, t, m] = i

                    else:
                        leastConsumedTime = math.inf
                        for s in range(S):
                            consumedTime = tau * math.ceil(M[m] / (tau * specBW[i, j, s, t]))
                            if t + consumedTime < T and ADJ_T[i, j, t, m] > consumedTime and LINK_EXISTS[
                                i, j, s, t, (t + consumedTime)] < math.inf:
                                ADJ_T[i, j, t, m] = consumedTime
                                Spectrum[i, j, t, m] = s + 1
                                Parent[i, j, t, m] = i


                    # if (t + leastConsumedTime < T):
                    #
                    #     # print(str(i) + " " + str(j) + " "  + str(s) + " " + str(t) + " " + str(t+consumedTime) + " " + str(LINK_EXISTS[ i, j, s, t, (t + consumedTime)]));
                    #     ADJ_T[i, j, t, m] = leastConsumedTime
                    #     Parent[i, j, t, m] = i

                    if (t + tau) < T and ADJ_T[i, j, t, m] == math.inf and ADJ_T[i, j, (t + tau), m] != math.inf:
                        ADJ_T[i, j, t, m] = ADJ_T[i, j, (t + tau), m] + tau
                        Parent[i, j, t, m] = Parent[i, j, t + tau, m]
                        Spectrum[i, j, t, m] = Spectrum[i, j, t + tau, m] + 10
                        #Spectrum[i, j, t, m] = 10

    return ADJ_T, Parent, Spectrum


# Determines the Least Latency Cost (LLC) Path for all messages in the STB graph
def LLC_PATH_ADJ_2(ADJ_T, Parent, Spectrum, V, S, T, M, tau):
    # LLC = Least Latency Cost Path
    # LLC_PATH = numpy.empty(shape=(V, V, T, len(M)))
    # LLC_PATH.fill(math.inf)

    #print("k i j t : LLC Parent")
    for m in range(len(M)):
        for k in range(V):
            for i in range(V):
                for j in range(V):
                    for t in range(T):
                        # leastTime = LLC_PATH[i, j, t, m]
                        #leastTime = math.inf

                        dcurr = ADJ_T[i, j, t, m]
                        d2 = math.inf
                        # dalt = math.inf

                        d1 = ADJ_T[i, k, t, m]
                        if d1 < math.inf and (t + d1) < T:
                            d2 = ADJ_T[k, j, (t + int(d1)), m]

                        if d1 + d2 < dcurr:
                            ADJ_T[i, j, t, m] = d1 + d2
                            Parent[i, j, t, m] = Parent[k, j, (t + int(d1)), m]
                            Spectrum[i, j, t, m] = Spectrum[k, j, (t + int(d1)), m]
                            if i ==0 and j == 2 and t  == 0:
                                print(str(k) + " " + str(i) + " " + str(j) + " " + str(t) + " : " + str(
                                                ADJ_T[i, j, t, m]) + " " + str(Parent[i, j, t, m]))

    return ADJ_T, Parent, Spectrum

