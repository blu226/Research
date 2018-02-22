import numpy
from createSTBGraph import *


# Print 5D adjacency matrix for the STB graph
def printADJ(ADJ_E, V, S, T, tau):
    print ("i j s ts te E")
    for i in range(V):
        for j in range(V):
            for s in range(S):
                for ts in range(0,T,tau):
                    for te in range(ts+tau, T, tau):
                        if i != j:
                            print(str(i) + " " + str(j) + " "  + str(s) + " " + str(ts) + " "  + str(te) +" = " + str(ADJ_E[i,j,s,ts,te]))

def print4d(adj):
    print("i j ts te x")
    for i in range(len(adj)):
        for j in range(len(adj[0])):
            for ts in range(len(adj[0][0])):
                for te in range(len(adj[0][0][0])):
                    if(adj[i,j,ts,te] != -1 and adj[i,j,ts,te] != math.inf):
                        print(str(i) + " " + str(j) +  " " + str(ts) + " "  + str(te) +" = " + str(adj[i,j,ts,te]))


# Determines the Least Energy Cost (LEC) Path for all messages in the STB graph
def LEC_PATH_ADJ(ADJ, V, S, T, tau):
    #LEC = Least Energy Cost Path
    LEC_PATH = numpy.empty(shape=(V, V, T, T))
    LEC_PATH.fill(-1)
    Parent = numpy.empty(shape=(V, V, T, T))
    Parent.fill(-1)
    Spectrum = numpy.empty(shape=(V, V, T, T))
    Spectrum.fill(-1)

    for k in range(V):
        for i in range(V):
            for j in range(V):
                for s1 in range(S):
                    for s2 in range(S):
                        for s3 in range(S):
                            for ts in range(0, T - tau  - 1, tau):
                                for te in range(ts + tau, T - 1, tau):
                                    for t in range(tau, te - tau, tau):
                                        if ts + t > te:             #Not a valid intermediate time interval
                                            continue

                                        if ( i != j):
                                            dcurr = ADJ[i][j][s1][ts][te]
                                            # print ("ts: " + str(t) + " ts+t: " +  str(ts + t))
                                            d1 = ADJ[i][k][s2][ts][ts + t]
                                            d2 = ADJ[k][j][s3][ts + t][te]
                                        
                                            if (dcurr > d1 + d2):
                                                LEC_PATH[i][j][ts][te] = d1 + d2
                                                Spectrum[i][k][ts][ts +t] = s2
                                                Spectrum[k][j][ts + t][te] = s3
                                                Parent[i][j][ts][te] = Parent[k][j][ts][te]
                                            else:
                                                LEC_PATH[i][j][ts][te] = dcurr
                                                Parent[i][j][ts][te] = i
                                                Spectrum[i][j][ts][te] = s1

    return LEC_PATH, Parent, Spectrum
