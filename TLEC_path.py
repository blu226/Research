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
    ADJ_TE = numpy.empty(shape=(V, V, T, TTL, len(M)))
    ADJ_TE.fill(math.inf)

    ADJ_TL = numpy.empty(shape=(V, V, T, TTL, len(M)))
    ADJ_TL.fill(math.inf)

    Parent_TE = numpy.empty(shape=(V, V, T, TTL, len(M)))
    Parent_TE.fill(-1)

    Spectrum_TE = numpy.empty(shape=(V, V, T, TTL, len(M)))
    Spectrum_TE.fill(-1)

    # print ("M   i  j  s  ts  te :  Val  cT  LExi   BW    ")
    for m in range(len(M)):
        for t in range(T - tau, -1, -tau):
            for i in range(V):
                for j in range(V):
                    for dt in range(TTL - tau, -1, -tau):

                        if i == j:
                            ADJ_TE[i, j, t, dt, m] = epsilon
                            ADJ_TL[i, j, t, dt, m] = tau
                            Parent_TE[i, j, t, dt, m] = i
                            Spectrum_TE[i, j, t, dt, m] = 10


                        else:
                            #minEnergy = math.inf
                            for s in range(S):
                                consumedTime = tau * math.ceil(M[m] / (tau * specBW[i, j, s, t]))
                                consumedEnergy = (M[m] / (specBW[i, j, s, t])) * spectPower[s]
                                consumedEnergy = round(consumedEnergy, 2)

                                # t + consumedTime < t + TTL is equivalent to first condition
                                if consumedTime <= dt and t + consumedTime < T and consumedEnergy < ADJ_TE[i, j, t, dt, m] and \
                                                LINK_EXISTS[i, j, s, t, (t + consumedTime)] < math.inf:
                                    #minEnergy = consumedEnergy
                                    ADJ_TE[i, j, t, dt, m] = consumedEnergy
                                    ADJ_TL[i, j, t, dt, m] = consumedTime
                                    Parent_TE[i, j, t, dt, m] = i
                                    Spectrum_TE[i, j, t, dt, m] = s + 1

                        #No spatial between i and j at time t, see if there exists a spatial link between them
                        # at time (t + tau)
                        if  (t + tau) < T and ADJ_TL[i, j, (t + tau), dt, m] + tau <= dt and ADJ_TE[i, j, t, dt, m] == math.inf and ADJ_TE[i, j, (t + tau), dt, m] != math.inf:
                            ADJ_TE[i, j, t, dt, m] = ADJ_TE[i, j, (t + tau), dt, m] + epsilon
                            ADJ_TL[i, j, t, dt, m] = ADJ_TL[i, j, (t + tau), dt, m] + tau
                            Parent_TE[i, j, t, dt, m] = Parent_TE[i, j, t + tau, dt, m]
                            Spectrum_TE[i, j, t, dt, m] = Spectrum_TE[i, j, t + tau, dt, m] +  10

    return ADJ_TE, Parent_TE, Spectrum_TE, ADJ_TL

# Determines the TTL constrained Energy-efficient Cost (TLEC) Path for all messages in the STB graph
def TLEC_PATH_ADJ_2(ADJ_TL, ADJ_TE, Parent_TE, Spectrum_TE):

    TLLC_PATH = ADJ_TL
    print("k i j t : TLEC Parent " + str(TTL) )
    for m in range(len(M)):
        for k in range(V):
            for i in range(V):
                for j in range(V):
                    for t in range(T):
                        for dt in range(TTL):
                            for dt1 in range(dt):

                                # dCurr = ADJ_T[i, j, t, m]
                                eCurr = ADJ_TE[i, j, t, dt, m]

                                # if dCurr > t + TTL:
                                #     ADJ_TE[i, j, t, m] = math.inf
                                #     eCurr = math.inf

                                e2 = math.inf
                                d2 = math.inf

                                e1 = ADJ_TE[i, k, t, dt1, m]
                                d1 = TLLC_PATH[i, k, t, dt1, m]

                                if d1 < math.inf and (t + d1) < T :
                                    d2 = TLLC_PATH[k, j, (t + int(d1)), (dt - dt1), m]
                                    e2 = ADJ_TE[k, j, (t + int(d1)), (dt - dt1), m]

                                eAlt = e1 + e2
                                dAlt = d1 + d2

                                if eAlt < eCurr and dAlt <= dt:
                                    ADJ_TE[i, j, t, dt, m] = eAlt
                                    TLLC_PATH[i, j, t, dt, m] = dAlt
                                    Parent_TE[i, j, t, dt, m] = Parent_TE[k, j, (t + int(d1)), (dt - dt1), m]
                                    Spectrum_TE[i, j, t, dt, m] = Spectrum_TE[k, j, (t + int(d1)), (dt - dt1), m]

    return ADJ_TE, Parent_TE, Spectrum_TE, TLLC_PATH


def PRINT_TLEC_PATH_FILE(TLEC_PATH, TLLC_PATH, Parent_TE, Spectrum_TE):
    m = 0

    file = open(path_to_folder + "TLEC_PATH.txt", "w")
    file2 = open(path_to_folder + "TLEC_PATH_SPECTRUM.txt", "w")
    #print("i j t m: PATH")
    for t in range(0, T, tau):
        for i in range(V):
            for j in range(V):
                # if i == 1 and j == 3:
                # print("\n" + str(i) + " " + str(j) + " " + str(t) + " " + str(m) + " " + str(
                #     TLEC_PATH[i, j, t, TTL - 1, m]) + " " + str(TLLC_PATH[i, j, t, TTL - 1, m]) + " : ", end=" ")

                if TLLC_PATH[i, j, t, TTL - 1, m] != math.inf:
                    d = t + int(TLLC_PATH[i, j, t, TTL - 1, m])  # total delay

                if TLLC_PATH[i, j, t, TTL - 1, m] != math.inf: #path exists
                    par_u = int(Parent_TE[i, j, t, TTL - 1, m])

                    path_str = str(j) + " "
                    print_path_str = str(j) + " "

                    d = d - tau

                    # temporal link
                    while d > t and Spectrum_TE[par_u, j, d, TTL - 1, m] > 10:
                        # Spectrum[par_u, j, d, m] -= 10
                        print_path_str += str(par_u) + " [" + str(Spectrum_TE[par_u, j, d, TTL - 1, m]) + ", " + str(d) + "] "
                        path_str += str(par_u) + " "
                        d = d - tau

                    old_par_u = j
                    while (par_u != -1 and par_u != i):

                        path_str += str(par_u) + " "
                        print_path_str += str(par_u) + " (" + str(Spectrum_TE[par_u, old_par_u, d, TTL - 1, m]) + ", " + str(d) + ") "

                        d = d - tau

                        # temporal link
                        while d > t and Spectrum_TE[par_u, old_par_u, d, TTL - 1, m] > 10:
                            # Spectrum[par_u, old_par_u, t, m] -= 10
                            print_path_str += str(par_u) + " [" + str(Spectrum_TE[par_u, old_par_u, d, TTL - 1, m]) + ", " + str(d) + "] "
                            path_str += str(par_u) + " "
                            d = d - tau

                        old_par_u = par_u
                        par_u = int(Parent_TE[i, par_u, t, TTL - 1, m])



                    path_str += str(i) + " "
                    print_path_str += str(i) + " (" +  str(Spectrum_TE[par_u, old_par_u, d, TTL - 1, m]) + ", " + str(d) +") "

                    d = d - tau
                    while d >= t and Spectrum_TE[i, old_par_u, d, TTL - 1, m] > 10:
                        # Spectrum[par_u, old_par_u, t, m] -= 10
                        print_path_str += str(i) + " [" + str(Spectrum_TE[i, old_par_u, d, TTL - 1, m]) + ", " + str(
                            d) + "] "
                        path_str += str(i) + " "
                        d = d - tau

                    # print (print_path_str, end = " ")
                    file.write(str(i) + " " + str(j) + " " + str(t) + " " + str(M[m]) + " " + path_str + "\n")
                    file2.write(str(i) + " " + str(j) + " " + str(t) + " " + str(M[m]) + " " +  str(
                    TLEC_PATH[i, j, t, TTL - 1, m]) + " " + str(TLLC_PATH[i, j, t, TTL - 1, m]) + " : " + print_path_str + "\n")
    file.close()
    file2.close()
