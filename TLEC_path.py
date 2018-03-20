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


# Determines the Least Latency Cost (LLC) Path for all messages in the STB graph
def TLEC_PATH_ADJ_2(ADJ_T, ADJ_TE, Parent_TE, Spectrum_TE):

    print("k i j t : LLC Parent " + str(TTL) )
    for m in range(len(M)):
        for k in range(V):
            for i in range(V):
                for j in range(V):
                    for t in range(T):

                        dCurr = ADJ_T[i, j, t, m]

                        if dCurr < t + TTL:
                            eCurr = ADJ_TE[i, j, t, m]
                        else:
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
                            #   Spectrum[i, j, t, m] = Spectrum[k, j, (t + int(d1)), m]
                        # if i ==3 and j == 0 and t  == 0:
                        #     print("Here " + str(k) + " " + str(i) + " " + str(j) + " " + str(t) + " : " + str(
                        #                     ADJ_TE[i, j, t, m]) + " " + str(Parent_TE[i, j, t, m]))

            # if i == j:
            #     Spectrum[i, j, t, m] = -1
                        # if i == 0 and j == 2 and t == 0 and m == 0:

                        # print("i: " + str(i) + " j: " + str(j) + " k: " + str(k) + " s1: " + str(
                        #     s1) + " s2: " + str(s2) + " s3: " + str(s3) + " t: " + str(t) + " m: " + str(m))
                        # print ("D: " + str(dcurr) +" d1: " + str(d1) + " d2: " + str(d2) + " " + str(LLC_PATH[i,j,t,m]) + "\n")

                            # if i == 0 and j == 3 and k == 1 and t == 0:
                            # print("Value here: " + str(LLC_PATH[0, 3, 0, 0]))
# print("Value here: " + str(LLC_PATH[0,3,0,0]))

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

                    with open("path.txt" , "a") as file:
                        file.write(str(i) + " " + str(j) + " " + str(t) + " " + str(M[m]) + " " + path_str + "\n")
    file.close()


