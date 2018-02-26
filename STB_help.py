import numpy
from createSTBGraph import *

def printADJ_4D (ADJ, V, T, M):
    for i in range(V):
        for j in range(V):
            for t in range(T):
               for m in range(len(M)):
                   print(str(i) + " " + str(j) + " " + str(t) + " " + str(M[m]) + " = " + str(ADJ[i, j, t, m]))


# Print Message Matrix
def printADJ_MSG(ADJ_MSG, V, S, T, M, tau):
    print ("i j s t m")
    for i in range(V):
        for j in range(V):
            for s in range(S):
                for t in range(T - tau, -1, -tau):
                    for m in range(len(M)):
                        if ADJ_MSG[i,j,s,t,m] != math.inf:
                            print(str(i) + " " + str(j) + " "  + str(s) + " " + str(t) + " "  + str(M[m]) +" = " + str(ADJ_MSG[i,j,s,t,m]))


# Print 5D adjacency matrix for the STB graph
def printADJ(ADJ_E, V, S, T, tau):
    print ("i j s ts te E")
    for i in range(V):
        for j in range(V):
            for s in range(S):
                for ts in range(0, T - tau, tau):
                    for te in range(ts + tau, T, tau):
                        #if ADJ_E[i, j, s, ts, te] != math.inf:
                        print(str(i) + " " + str(j) + " "  + str(s) + " " + str(ts) + " "  + str(te) +" = " + str(ADJ_E[i,j,s,ts,te]))

def print4d(adj):
    print("i j ts te x")
    for i in range(len(adj)):
        for j in range(len(adj[0])):
            for ts in range(len(adj[0][0])):
                for te in range(len(adj[0][0][0])):
                    if(adj[i,j,ts,te] != -1 and adj[i,j,ts,te] != math.inf):
                        print(str(i) + " " + str(j) +  " " + str(ts) + " "  + str(te) +" = " + str(adj[i,j,ts,te]))

# Get minimum of spectrum bandwidths available at two nodes i and j at time t
# This is important because we can only use the common channels (available at both the nodes) as the total bandwidth of the band
# Moreover, note that here we assumed that the channels available at the node (with lower bandwidth) is also existent at the node
# with higher bandwidth of a certain band
def getMinBWFromDMFiles(i, j, s, t):
    with open("Data/" + str(i) + ".txt") as fi:
        next(fi)
        iLines = fi.readlines()
    fi.close()

    with open("Data/" + str(j) + ".txt") as fj:
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
                if int(iLineArr[s + 3]) < int(jLineArr[s + 3]):
                    currBW = int(iLineArr[s + 3])
                    return currBW
                else:
                    currBW = int(jLineArr[s + 3])
                    return currBW
                    # else:
                    #     print (str(t) + " " + iLineArr[0] + " " + jLineArr[0])
    return currBW

# Compute tau defined as the least message transmission delay in transmitting a message of least size over the spectrum band with
# highest bandwidth across all times t = 0, 1, .... T
def computeTau():
    return 1

# Get the dynamic bandwidth of any given band in the set S, between any node pair at any time epoch t
def getSpecBW(specBW, V, S, T):
    for i in range(V):
        for j in range(V):
            for s in range(S):
                for t in range(T):
                    specBW[i, j, s, t] = getMinBWFromDMFiles(i, j, s, t)
                    # print ("SpecBW: i= " + str(i) + " j= " + str(j) + " s= " + str(s) + " t= " + str(t) + " BW= " + str(specBW[i, j, s, t]))
    return specBW


# Check if a pair of nodes i and j are sufficienctly in communication range over any band type s, starting at time ts until time te
def linkExists(i, j, s, ts, te):
    with open("Data/" + str(i) + ".txt") as fi:
        next(fi)
        iLines = fi.readlines()
    fi.close()

    with open("Data/" + str(j) + ".txt") as fj:
        next(fj)
        jLines = fj.readlines()
    fj.close()

    return True

# Compute the adjacency matrix : 1 if link exists, else 0
def initializeADJ(ADJ, V, S, T, tau, specBW):
    for i in range(V):
        for j in range(V):
            for s in range(S):
                for ts in range(0, T - tau, tau):
                    te = ts + tau  # Initialize te, however, based on message size, we get appropriate te later
                    if i != j:
                        for m in M:
                            # here the message transmission delay is equivalent to z (discussed in the paper)
                            msgTransDelay = math.ceil(m / (tau * specBW[i, j, s, ts]))
                            te = ts + msgTransDelay * tau  # End time epoch for current message m
                            # print ("M: " + str(m) + "  " + str(te))

                            if te >= T:
                                break
                            else:
                                if linkExists(i, j, s, ts, te) == True:
                                    ADJ[i, j, s, ts, te] = 1  # spatial link
                    else:
                        ADJ[i, j, s, ts, te] = 1  # Temporal Link - link exists between (t, t+tau)

    return ADJ

# Initialize the 5-D adjacency matrix where the value is 1 if
# node i and j are in communication range for a time period [ts, te] over any band s in the set S
# Assumption 1: Spectrum power and transmission range does not change
# Assumption 2: Only Spectrum bandwidth changes over time and location (i.e., at different nodes)
# Assumption 3: However given a bandwidth of a certain band at time t, it remains constant for the duration of transmission delay for any message
def initializeADJ_E(ADJ_E, V, S, T, tau, specBW):
    for i in range(V):
        for j in range(V):
            for s in range(S):
                for ts in range(0, T - tau, tau):
                    te = ts + tau  # Initialize te, however, based on message size, we get appropriate te later
                    if i != j:
                        for m in M:
                            # here the message transmission delay is equivalent to z (discussed in the paper)
                            msgTransDelay = math.ceil(m / (tau * specBW[i, j, s, ts]))
                            te = ts + msgTransDelay * tau  # End time epoch for current message m

                            if te >= T:
                                break
                            else:
                                consEnergy = msgTransDelay * spectPower[s] * tau
                                if linkExists(i, j, s, ts, te) == True:
                                    ADJ_E[i, j, s, ts, te] = consEnergy  # spatial link
                    else:
                        ADJ_E[i, j, s, ts, te] = 0  # Temporal Link - Energy consumed is 0

    return ADJ_E


# Compute message colors (i.e., message transmission delays) for spatial links (ONLY SPATIAL LINKS)
def computeADJ_MSG(specBW, ADJ_MSG, ADJ, V, S, T, M, tau):
    for t in range(T - tau, -1, -tau):
        for i in range(V):
            for j in range(V):
                for s in range(S):
                    for m in range(len(M)):
                        # print (str(i) + " " + str(j) + " " + str(s) + " " + str(t) + " " + str(m) + " "+ str(specBW[i, j, s, t]))
                        consumedTime = tau * math.ceil(M[m] / (tau * specBW[i, j, s, t]))
                        if i == j:
                            consumedTime = tau

                        if (t + consumedTime < T) and ADJ[i, j, s, t, (t + consumedTime)] == 1:
                            ADJ_MSG[i, j, s, t, m] = consumedTime
                        elif (t + tau) < T and ADJ_MSG[i, j, s, (t + tau), m] != math.inf:
                            ADJ_MSG[i, j, s, t, m] = ADJ_MSG[i, j, s, (t + tau), m] + tau
                        else:
                            ADJ_MSG[i, j, s, t, m] = math.inf
    return ADJ_MSG


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
                            for t in range(0, T, tau):
                                for ts in range(0, T, tau):
                                    for te in range(ts + tau, T, tau):
                                        if ts + t >= te:             #Not a valid intermediate time interval
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


# Determines the Least Latency Cost (LLC) Path for all messages in the STB graph
def LLC_PATH_ADJ(ADJ, ADJ_MSG, V, S, T, M, tau):

    # LLC = Least Latency Cost Path
    LLC_PATH = numpy.empty(shape=(V, V, T, len(M)))
    LLC_PATH.fill(math.inf)
    Parent = numpy.empty(shape=(V, V, T, len(M)))
    Parent.fill(-1)
    Spectrum = numpy.empty(shape=(V, V, T, len(M)))
    Spectrum.fill(-1)

    for m in range(len(M)):
        for k in range(V):
            for i in range(V):
                for j in range(V):
                    for t in range(0, T, tau):
                        leastTime = math.inf
                        for s1 in range(S):
                            for s2 in range(S):
                                for s3 in range(S):

                                    dcurr = ADJ_MSG[i, j, s1, t, m]
                                    d1 = ADJ_MSG[i, k, s2, t, m]
                                    if d1 == math.inf or (d1 != math.inf and t + d1 > T):
                                        d2 = math.inf
                                    else:
                                        d2 = ADJ_MSG[k, j, s3, (t + int(d1)), m]

                                    dalt = d1 + d2
                                    # print ("D: " + str(dcurr) +" d1: " + str(d1) + " d2: " + str(d2))

                                    if dalt <= dcurr and dalt < leastTime:
                                        leastTime = dalt
                                        LLC_PATH[i, j, t, m] = leastTime
                                        Spectrum[i, k, t, m] = s2
                                        Spectrum[k, j, t, m] = s3
                                        Parent[i, j, t, m] = Parent[k, j, t, m]

                                    elif dcurr <= dalt and dcurr < leastTime:
                                        leastTime = dcurr
                                        LLC_PATH[i, j, t, m] = leastTime
                                        Parent[i, j, t, m] = i
                                        Spectrum[i, j, t, m] = s1

                    # print(str(i) + " " + str(j) + " " + str(M[m]) + " = " + str(ADJ[i, j, m]))

    return LLC_PATH, Parent, Spectrum