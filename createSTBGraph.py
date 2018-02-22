import math
from constants import *

# Compute tau defined as the least message transmission delay in transmitting a message of least size over the spectrum band with
# highest bandwidth across all times t = 0, 1, .... T
def computeTau():
    return 1

# Get minimum of spectrum bandwidths available at two nodes i and j at time t
# This is important because we can only use the common channels (available at both the nodes) as the total bandwidth of the band
# Moreover, note that here we assumed that the channels available at the node (with lower bandwidth) is also existent at the node
# with higher bandwidth of a certain band
def getMinBWFromDMFiles(i, j, s, t):
    with open("Data/"+ str(i) + ".txt") as fi:
        next(fi)
        iLines = fi.readlines()
    fi.close()

    with open("Data/"+ str(j) + ".txt") as fj:
        next(fj)
        jLines = fj.readlines()
    fj.close()

    currBW = -1
    for iLine in iLines:
        iLineArr = iLine.strip().split(' ')
        for jLine in jLines:
            jLineArr = jLine.strip().split(' ')
            # print ("At time " + str(t) + " Values: " + iLineArr[0] + " " + jLineArr[0])
            if int(iLineArr[0]) == t and int(jLineArr[0]) == t:
                # print("At time " + str(t) + " Values: " + iLineArr[3] + " " + jLineArr[3])
                if int(iLineArr[s+3]) < int(jLineArr[s+3]):
                    currBW = int(iLineArr[s+3])
                    return currBW
                else:
                    currBW = int(jLineArr[s+3])
                    return currBW
            # else:
            #     print (str(t) + " " + iLineArr[0] + " " + jLineArr[0])
    return currBW


# Get the dynamic bandwidth of any given band in the set S, between any node pair at any time epoch t
def getSpecBW(specBW, V, S, T):
    for i in range(V):
        for j in range(V):
            for s in range(S):
                for t in range(T):
                    if i == j:
                        specBW[i, j, s, t] = 0
                    else:
                        specBW[i, j, s, t] = getMinBWFromDMFiles(i, j, s, t)
                        # print ("SpecBW: i= " + str(i) + " j= " + str(j) + " s= " + str(s) + " t= " + str(t) + " BW= " + str(specBW[i, j, s, t]))
    return specBW

# Check if a pair of nodes i and j are sufficienctly in communication range over any band type s, starting at time ts until time te
def linkExists(i, j, s, ts , te):
    with open("Data/" + str(i) + ".txt") as fi:
        next(fi)
        iLines = fi.readlines()
    fi.close()

    with open("Data/" + str(j) + ".txt") as fj:
        next(fj)
        jLines = fj.readlines()
    fj.close()

    return True


# Initialize the 5-D adjacency matrix where the value is 1 if
# node i and j are in communication range for a time period [ts, te] over any band s in the set S
# Assumption 1: Spectrum power and transmission range does not change
# Assumption 2: Only Spectrum bandwidth changes over time and location (i.e., at different nodes)
# Assumption 3: However given a bandwidth of a certain band at time t, it remains constant for the duration of transmission delay for any message
def initializeADJ(ADJ_E, V, S, T, tau, specBW):
    for i in range(V):
        for j in range(V):
            for s in range(S):
                for ts in range(0, T, tau):
                    te = ts + tau
                    if i != j:
                        for m in M:
                            # here the message transmission delay is equivalent to z (discussed in the paper)
                            msgTransDelay = math.ceil(m / (tau * specBW[i, j, s, ts]))
                            te = ts + msgTransDelay * tau    # End time epoch for current message m
                            if te >= T:
                                break
                            else:
                                consEnergy = msgTransDelay * spectPower[s] * tau
                                if linkExists(i, j, s, ts, te) == True:
                                    ADJ_E[i,j,s,ts,te] =  consEnergy            # spatial link

    return ADJ_E


# V = NoOfDMs                 # Number of nodes in the STB graph is equivalent to number of data mules we have in the DSA overlay network
# specBW = numpy.zeros(shape =(V, V, S, T))
# ADJ_E = numpy.empty(shape=(V, V, S, T, T))
# ADJ_E.fill(math.inf)
#
# tau = computeTau()
# specBW = getSpecBW(specBW, V, S, T)

# ADJ_E = initializeADJ(ADJ_E, V, S, T, tau)
# printADJ(ADJ_E, V, S, T, tau)






