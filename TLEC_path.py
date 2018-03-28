import numpy
import math
from STB_help import *
from constants import *

# Compute message colors (i.e., message transmission delays) for spatial links (ONLY SPATIAL LINKS)
def computeADJ_TE_2(specBW, LINK_EXISTS, tau):
    ADJ_TE = numpy.empty(shape=(V, V, T, len(M)))
    ADJ_TE.fill(math.inf)

    Parent_TE = numpy.empty(shape=(V, V, T, len(M)))
    Parent_TE.fill(-1)

    Spectrum_TE = numpy.empty(shape=(V, V, T, len(M)))
    Spectrum_TE.fill(-1)

    # print ("M   i  j  s  ts  te :  Val  cT  LExi   BW    ")
    for m in range(len(M)):
        for t in range(T - tau, -1, -tau):
            for i in range(V):
                for j in range(V):

                    if i == j:
                        ADJ_TE[i, j, t, m] = epsilon
                        Parent_TE[i, j, t, m] = i
                        Spectrum_TE[i, j, t, m] = -2

                    else:
                        #minEnergy = math.inf
                        for s in range(S):
                            consumedTime = tau * math.ceil(M[m] / (tau * specBW[i, j, s, t]))
                            consumedEnergy = (M[m] / (specBW[i, j, s, t])) * spectPower[s]
                            consumedEnergy = round(consumedEnergy, 2)

                            if ADJ_TE[i, j, t, m] > consumedEnergy and consumedTime < TTL and t + consumedTime < T and \
                                            LINK_EXISTS[i, j, s, t, (t + consumedTime)] < math.inf:
                                #minEnergy = consumedEnergy
                                ADJ_TE[i, j, t, m] = consumedEnergy
                                Parent_TE[i, j, t, m] = i
                                Spectrum_TE[i, j, t, m] = s

                    if (t + tau) < T and tau < TTL and ADJ_TE[i, j, t, m] == math.inf and ADJ_TE[i, j, (t + tau), m] != math.inf:
                        ADJ_TE[i, j, t, m] = ADJ_TE[i, j, (t + tau), m] + epsilon
                        Parent_TE[i, j, t, m] = Parent_TE[i, j, t + tau, m]
                        Spectrum_TE[i, j, t, m] = 9

    return ADJ_TE, Parent_TE, Spectrum_TE



# Compute message colors (i.e., message transmission delays) for spatial links (ONLY SPATIAL LINKS)
def computeADJ_T_TE(specBW, LINK_EXISTS, tau):
    ADJ_TE = numpy.empty(shape=(V, V, T, len(M)))
    ADJ_TE.fill(math.inf)

    ADJ_T = numpy.empty(shape=(V, V, T, len(M)))
    ADJ_T.fill(math.inf)


    Parent_TE = numpy.empty(shape=(V, V, T, len(M)))
    Parent_TE.fill(-1)

    Spectrum_TE = numpy.empty(shape=(V, V, T, len(M)))
    Spectrum_TE.fill(-1)

    # print ("M   i  j  s  ts  te :  Val  cT  LExi   BW    ")
    for m in range(len(M)):
        for t in range(T - tau, -1, -tau):
            for i in range(V):
                for j in range(V):

                    if i == j:
                        ADJ_TE[i, j, t, m] = epsilon
                        Parent_TE[i, j, t, m] = i
                        #Spectrum_TE[i, j, t, m] = -2

                    else:
                        #minEnergy = math.inf
                        for s in range(S):
                            consumedTime = tau * math.ceil(M[m] / (tau * specBW[i, j, s, t]))
                            consumedEnergy = (M[m] / (specBW[i, j, s, t])) * spectPower[s]
                            consumedEnergy = round(consumedEnergy, 2)

                            # t + consumedTime < t + TTL is equivalent to first condition
                            if consumedTime < TTL and t + consumedTime < T and consumedEnergy < ADJ_TE[i, j, t, m] and \
                                            LINK_EXISTS[i, j, s, t, (t + consumedTime)] < math.inf:
                                #minEnergy = consumedEnergy
                                ADJ_TE[i, j, t, m] = consumedEnergy
                                ADJ_T[i, j, t, m] = consumedTime
                                Parent_TE[i, j, t, m] = i
                                Spectrum_TE[i, j, t, m] = s

                    #No spatial between i and j at time t, see if there exists a spatial link between them
                    # at time (t + tau)
                    if tau < TTL  and (t + tau) < T and ADJ_TE[i, j, t, m] == math.inf and ADJ_TE[i, j, (t + tau), m] != math.inf:
                        ADJ_TE[i, j, t, m] = ADJ_TE[i, j, (t + tau), m] + epsilon
                        ADJ_T[i, j, t, m] = ADJ_T[i, j, (t + tau), m] + tau
                        Parent_TE[i, j, t, m] = Parent_TE[i, j, t + tau, m]
                        Spectrum_TE[i, j, t, m] = Spectrum_TE[i, j, t + tau, m] +  10

    return ADJ_TE, Parent_TE, Spectrum_TE, ADJ_T

# Determines the TTL constrained Energy-efficient Cost (TLEC) Path for all messages in the STB graph
def TLEC_PATH_ADJ_2(ADJ_T, ADJ_TE, Parent_TE, Spectrum_TE):

    print("k i j t : LLC Parent " + str(TTL) )
    for m in range(len(M)):
        for k in range(V):
            for i in range(V):
                for j in range(V):
                    for t in range(T):

                        dCurr = ADJ_T[i, j, t, m]
                        eCurr = ADJ_TE[i, j, t, m]

                        if dCurr > t + TTL:
                            eCurr = math.inf

                        e2 = math.inf
                        d2 = math.inf

                        e1 = ADJ_TE[i, k, t, m]
                        d1 = ADJ_T[i, k, t, m]

                        if (t + d1) < T:
                            d2 = ADJ_T[k, j, (t + int(d1)), m]
                            e2 = ADJ_TE[k, j, (t + int(d1)), m]

                        eAlt = e1 + e2
                        dAlt = d1 + d2

                        if eAlt < eCurr and dAlt < TTL:
                            ADJ_TE[i, j, t, m] = eAlt
                            Parent_TE[i, j, t, m] = Parent_TE[k, j, (t + int(d1)), m]

    return ADJ_TE, Parent_TE, Spectrum_TE

def PRINT_PATH_2(LLC_PATH, Parent, Spectrum):
    V = NoOfDMs
    m = 0
    tau = 1

    print("i j t m: PATH")
    for t in range(T):
        for i in range(V):
            for j in range(V):
                # if i == 1 and j == 3:
                print("\n" + str(i) + " " + str(j) + " " + str(t) + " " + str(M[0]) + " " + str(LLC_PATH[i, j, t, m]) + " ", end=" ")
                # print("Path from " + str(u) + " -> "+ str(v) + " at time " + str(t) + " for message 0 is")
                if LLC_PATH[i, j, t, m] != math.inf:
                    #delivered = delivered + 1
                    par_u = int(Parent[i, j, t, m])

                    path_str = str(j)+ " (" + str(int(Spectrum[par_u, j, t, m])) + ") " + " <- "
                    # ts = t + tau

                    while par_u != -1  and t < T and (par_u != i or (par_u == i and Spectrum[par_u, j, t, m] < S and Spectrum[i, par_u, t, m] < S)):

                        if par_u == i and Spectrum[par_u, j, t, m] < S:
                            break

                        oldPar_u = par_u
                        #count_hops = count_hops + 1
                        path_str += str(par_u)
                        par_u = int(Parent[i, par_u, t, m])

                        # if i == 1 and j == 3:
                        # print ("\nOld: " + str(oldPar_u) + " New: " + str(par_u) + " Spec: " + str(Spectrum[oldPar_u, par_u, t, m]))

                        if Spectrum[oldPar_u, par_u, t, m] > S:
                           Spectrum[oldPar_u, par_u, t, m] = Spectrum[oldPar_u, par_u, t, m] - 10

                        path_str +=  " (" + str(int(Spectrum[oldPar_u,par_u, t, m])) + ") " + " <- "


                    path_str += str(i)
                    # if i == 1 and j == 3:
                    print (path_str, end = " ")





def PRINT_PATH_FILE(LLC_PATH, Parent, Spectrum):
    V = NoOfDMs
    m = 0
    tau = 1

    #print("i j t m: PATH")
    for t in range(T):
        for i in range(V):
            for j in range(V):
                # if i == 1 and j == 3:
                print("\n" + str(i) + " " + str(j) + " " + str(t) + " " + str(M[0])+ " ", end=" ")
                # print("Path from " + str(u) + " -> "+ str(v) + " at time " + str(t) + " for message 0 is")
                if LLC_PATH[i, j, t, m] != math.inf:
                    #delivered = delivered + 1
                    par_u = int(Parent[i, j, t, m])

                    path_str = str(j) + " "
                    # ts = t + tau

                    while par_u != -1  and t < T and par_u != i:

                        path_str += str(par_u) + " "
                        par_u = int(Parent[i, par_u, t, m])

                    path_str += str(i) + " "

                    print (path_str, end = " ")

                    # with open("path.txt" , "a") as file:
                    #     file.write(str(i) + " " + str(j) + " " + str(t) + " " + str(M[m]) + " " + path_str + "\n")
    file.close()


