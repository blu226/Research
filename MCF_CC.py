#Minimum Cost Flow Cycle Cancelling Algorithm

#inputs: U = 2D matrix containing max capacity of edge between nodes
#	 C = 2D matrix containing cost of edge between nodes
#	 F = 2D matrix containing a feasible solution of the minimum cost flow

import math

def residual(U, C, F):						#create residual graph based on a feasible solution

    for i in range(len(U)):
        for j in range(len(U)):
            if (F[i][j] != 0):					#if there is flow from i to j
                F[j][i] = F[i][j]				#create residual path from j to i
                C[j][i] = -C[i][j]
                U[i][j] = U[i][j] - F[i][j] 			#update max capacity of edge

def edge_dict(C):						#create a dict for the bellman ford function (not tested)
    d = {}
    for i in range(len(C)):
        t = {}
        for j in range(len(C)):
            if C[i][j] != 0:
                t[j] = C[i][j]
        d[i] = t
    return d

def initialize(graph, source):
    d = {} # Stands for destination
    p = {} # Stands for predecessor
    for node in graph:
        d[node] = float('Inf') # We start admiting that the rest of nodes are very very far
        p[node] = None
    d[source] = 0 # For the source we know how to reach
    return d, p

def relax(node, neighbour, graph, d, p):
    # If the distance between the node and the neighbour is lower than the one I have now
    if d[neighbour] > d[node] + graph[node][neighbour]:
        # Record this lower distance
        d[neighbour]  = d[node] + graph[node][neighbour]
        p[neighbour] = node

def bellman_ford(graph, source):
    d, p = initialize(graph, source)
    for i in range(len(graph)-1): #Run this until is converges
        for u in graph:
            for v in graph[u]: #For each neighbour of u
                relax(u, v, graph, d, p) #Lets relax it

    # Step 3: check for negative-weight cycles
    for u in graph:
        for v in graph[u]:
            assert d[v] <= d[u] + graph[u][v]

    return d, p

def MCF(U, C, F):
   #create residual graph
    residual(U, C, F)
   #check for negative cycles
   #if a negative cycle exists augment the residual network 
