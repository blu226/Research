import random
import math
#--------------------------------------------------------------------------------------------------------------------------------
#OTHER FUNCTIONS
def print_3Dmatrix(adj):
    for i in range(len(adj)):
        for j in range(len(adj)):
            print(adj[i][j], " ")
        print()
#--------------------------------------------------------------------------------------------------------------------------------
def print_networkmap(adj):                                                              #function to clearly show the details of the
    print("Network Map")                                                                #the nodes in the network and the weights
    for i in range(len(adj)):                                                           #between each node
        print("Node ", i, ":")
        for j in range(len(adj[i])):
            print("\t node ", j)
            for k in range(len(adj[i][j])):
                print("\t\t -Spectrum ", k, ": ", adj[i][j][k])
#----------------------------------------------------------------------------------------------------------------------------------
def create_adj(nodes, spectrums):                                                       #function to randomly generate 3D adj matrix
    max_weight = 20                                                                     #set a maximum weight for edges
    min_weight = 5                                                                      #set a min weight > 0 for edges
    step = 5                                                                            #step interval for random numbers
    adj = [[[random.randrange(min_weight, max_weight, step) for x in range(spectrums)] for y in range(nodes)] for z in range(nodes)] #cr$
    for i in range(len(adj)):                                                           #set 0 for "edges" to the same node
        for j in range(spectrums):
            adj[i][i][j] = 0
    return adj

    for i in range(len(adj)):                                                           #OPTIONAL for loop to make edges bidirectional
        for j in range(len(adj)):                                                       #in a way such that the weight(i, j) = weight(j,$
            for z in range(spectrums):
                adj[j][i][z] = adj[i][j][z]
    for i in range((nodes*spectrums)):                                               #OPTIONAL for loop to randomly place edges with
        x = random.randrange(0,nodes,1)                                                 #a weight of 0 into the adj matrix
        y = random.randrange(0,nodes,1)
        for j in range(spectrums):
            adj[x][y][j] = 0
            adj[y][x][j] = 0

#    return adj                                                                         #return a 3D list
#--------------------------------------------------------------------------------------------------------------------------------
def dfs(F, s, t, matrix):                                                               #DFS function [flow matrix, source, sink]
    num_spectrums = len(matrix[0][0])
    stack = [s]                                                                         #create stack to keep track of where to go
    paths = {s: []}                                                                     #create path dict to keep track of paths
    if s == t:                                                                          #checks if source = destination
        return paths[s]
    while stack:                                                                        #while loop to find paths while stack isn't empty
        cur = stack.pop()                                                               #create variable for current node being traversed
        for i in range(len(F)):
            for j in range(num_spectrums):
                if (matrix[cur][i][j]-F[cur][i][j] > 0) and i not in paths:             #check if there is a path
                    paths[i] = paths[cur] + [(cur,i,j)]                                 #add path to dict
                    if i == t:                                                          #check if sink node has been reached
                        return paths[i]                                                 #if sink has been reached return path found
                    stack.append(i)                                                     #add node with edge to stack to be traversed
    return "None"
#--------------------------------------------------------------------------------------------------------------------------------
def ford_fulkerson(s, t, matrix):                                                       #Ford and Fulkerson function [source, sink, matr$
    paths = []
    F = [[[0]*(len(matrix[0][0])) for i in range(len(matrix))] for j in range(len(matrix))]   #create identical sized graph to keep trac$
    path = dfs(F, s, t, matrix)                                                         #find first path using DFS
    while path != "None":                                                               #loop while a path still exists
        paths.append(path)
        flow = min(matrix[u][v][i] - F[u][v][i] for u,v,i in path)                      #find flow value
        for u,v,i in path:                                                              #update flow matrix
            F[u][v][i] += flow
            F[v][u][i] -= flow
        path = dfs(F, s, t, matrix)                                                     #find new path
    max_flow = sum(F[s][i][0] for i in range(len(matrix)))                              #maximum flow
    return paths                                                                        #return paths found for max flow
#------------------------------------------------------------------------------------------------------------------------------
def find_paths(s, t, adj):                                                              #function to find maximum flow paths
    hops = []
    paths = ford_fulkerson(s, t, adj)                                                   #find max flow paths
    for i in range(len(paths)):                                                         #for each of the paths in the max flow
        temp = []                                                                       #create temp list to store hop data
        for x,y,z in paths[i]:                                                          #for each hop in a path
            src = x
            dst = y
            spec = z                                                                    #store each hop as a list containing
            hop = [src, dst, spec]                                                      #[source, destination/next hop, spectrum]
            temp.append(hop)                                                            #add hop to path list
        hops.append(temp)                                                               #add path to paths list
    return hops                                                                         #return list of paths
#-------------------------------------------------------------------------------------------------------------------------------
def floyd_warshall(adj):                                                                #Floyd-Warshall function
    length = len(adj)
    num_spectrums = len(adj[0][0])
    inf = 1000                                                                          #variable to simulate infinity
    dist = [[[inf]*num_spectrums for i in range(length)] for j in range(length)]        #create a distance matrix the same size
    for i in range(length):                                                             #as adj and add edges if they exist
        for j in range(length):
            for s in range(num_spectrums):
                if (adj[i][j][s] != 0 and adj[i][j][s] < dist[i][j][s]):
                    dist[i][j][s] = adj[i][j][s]
    for k in range(length):                                                             #for each intermediate node k between i and j
        for i in range(length):                                                         #check to see the path from i to k to j is
            for j in range(length):                                                     #shorter than the path from i to j
                for s in range(num_spectrums):
                    if (dist[i][j][s] > (dist[i][k][s] + dist[k][j][s]) and (i != j)):  #if so and i != j
                        dist[i][j][s] = dist[i][k][s] + dist[k][j][s]                   #update the distance matrix
    for i in range(length):                                                             #set the weight from a node to itself as 0
        for j in range(length):
            if i == j:
                for s in range(num_spectrums):
                    dist[i][j][s] = 0
    return dist
#---------------------------------------------------------------------------------------------------------------------------------
def distance(n1, n2):									#Find distance between 2 nodes
    x1 = n1.coord[0]
    y1 = n1.coord[1]
    x2 = n2.coord[0]
    y2 = n2.coord[1]

    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance
#---------------------------------------------------------------------------------------------------------------------------------
def dist_matrix(nodes):
    length = len(nodes)
    dist = [[0 for i in range(length)] for j in range(length)]
    for i in range(length):
        for j in range(length):
            dist[i][j] = distance(nodes[i], nodes[j])
    return dist
