from constants import *
from createSTBGraph import *

def print4d(adj):
    print("i j ts te x")
    for i in range(len(adj)):
        for j in range(len(adj[0])):
            for ts in range(len(adj[0][0])):
                for te in range(len(adj[0][0][0])):
                    if(adj[i,j,ts,te] != -1 and adj[i,j,ts,te] != math.inf):
                        print(str(i) + " " + str(j) +  " " + str(ts) + " "  + str(te) +" = " + str(adj[i,j,ts,te]))

def shortestPathADJ(ADJ, V, S, T, tau):

    ShortestPath = numpy.empty(shape=(V, V, T, T))
    ShortestPath.fill(-1)
    parent = numpy.empty(shape=(V, V, T, T))
    parent.fill(-1)
    spectrum = numpy.empty(shape=(V, V, T, T))
    spectrum.fill(-1)

    for k in range(V):
        for i in range(V):
            for j in range(V):
                for s1 in range(S):
                    for s2 in range(S):
                        for s3 in range(S):
                            for ts in range(0,T,tau):
                                for te in range(ts+tau, T, tau):
                                    for t in range(ts+tau, te, tau):
                                        if ( i != j):
                                            dcurr = ADJ[i][j][s1][ts][te]
                                            d1 = ADJ[i][k][s2][ts][ts + t]
                                            d2 = ADJ[k][j][s3][ts + t][te]
                                        
                                            if (dcurr > d1 + d2):
                                                ShortestPath[i][j][ts][te] = d1 + d2
                                                spectrum[i][k][ts][ts +t] = s2
                                                spectrum[k][j][ts + t][te] = s3
                                                parent[i][j][ts][te] = parent[k][j][ts][te]
                                            else:
                                                ShortestPath[i][j][ts][te] = dcurr
                                                parent[i][j][ts][te] = i
                                                spectrum[i][j][ts][te] = s1
    print("Shortest Path")
    print4d(ShortestPath)
    print("Parent")
    print4d(parent)
    print("Spectrum")
    print4d(spectrum)

    return ShortestPath

V = NoOfDMs                 # Number of nodes in the STB graph is equivalent to number of data mules we have in the DSA overlay network
specBW = numpy.zeros(shape =(V, V, S, T))
ADJ_E = numpy.empty(shape=(V, V, S, T, T))
ADJ_E.fill(math.inf)
ADJ_E = initializeADJ(ADJ_E, V, S, T, tau)


print("ADJ_E")
printADJ(ADJ_E, V, S, T, tau)

minPath = shortestPathADJ(ADJ_E, V, S, T, tau)
