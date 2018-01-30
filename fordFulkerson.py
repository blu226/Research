"""
Brian Luciano
December 2017
Purpose: Create a graph class to implement the Ford and Fulkerson algorithm

"""
class Graph(object):

    def __init__(self, nodes):
        self.nodes = nodes
        self.matrix = [[0 for i in range(nodes)] for j in range(nodes)]

    def add_edge(self, start, to, weight):
        self.matrix[start][to] = weight

    def print_graph(self):
        print(self.matrix)


    def dfs(self, F, s, t):                                                     #DFS function [flow matrix, source, sink]
        stack = [s]                                                             #create stack to keep track of where to go
        paths = {s: []}                                                         #create path dict to keep track of paths
        if s == t:                                                              #checks if source = destination
            return paths[s]
        while stack:                                                            #while loop to find paths while stack isn't empty
            print(paths)
            cur = stack.pop()                                                   #create variable for current node being traversed
            for i in range(self.nodes):
                if (self.matrix[cur][i]-F[cur][i] > 0) and i not in paths:      #check if there is a path
                    paths[i] = paths[cur] + [(cur,i)]                           #add path to dict
                    if i == t:                                                  #check if sink node has been reached
                        return paths[i]
                    stack.append(i)                                             #add node with edge to stack to be traversed
        print(paths)
        return "None"

    def ford_fulkerson(self,s,t):                                               #Ford and Fulkerson function [source, sink]
        F = [[0]*self.nodes for i in range(self.nodes)]                         #create identical sized graph to keep track of flow
        path = self.dfs(F,s,t)                                                  #find first path using DFS
        while path != "None":                                                   #loop while a path still exists
            flow = min(self.matrix[u][v] - F[u][v] for u,v in path)             #find flow value
            for u,v in path:                                                    #update flow matrix
                F[u][v] += flow
                F[v][u] -= flow
            path = self.dfs(F,s,t)                                              #find new path
            print(F)
        return sum(F[s][i] for i in range(self.nodes))                          #return the sum of flows


def main():
    print("Ford Fulkerson Maximum Flow\n")
#    num = input("Enter # of nodes in graph(including source and sink): ")
#    while num.isalpha():
#        print("Must input int")
#        num = input("Enter # of nodes in graph(including source and sink): ")
    g = Graph(4)
    g.add_edge(0,1,5)
    g.add_edge(0,2,5)
    g.add_edge(1,2,5)
    g.add_edge(1,3,4)
    g.add_edge(2,3,3)


#    print("Nodes are numbered 0 to [number of nodes] - 1")
#    answer = input("press 'y' to add an edge to the graph, or 'q' to continue: ")
#    while answer != "q":
#        s = input("Enter source node: ")
#        while (s.isalpha() or s >= num):
#            print("Must input int between 0 and ", num - 1)
#            s = input("Enter source node: ")
#        d = input("Enter destination node: ")
#        while (d.isalpha() or s >= num):
#            print("Must input int between 0 and ", num - 1)
#            d = input("Enter destination node: ")
#        w = input("Enter weight of edge: ")
#        while (w.isalpha() or int(w) < 0):
#            print("Must input int > 0")
#            w = input("Enter weight of edge: ")
#        g.add_edge(int(s), int(d), int(w))
#        answer = input("Press 'y' to add another edge, or 'q' to find out your max flow: ")

    flow = g.ford_fulkerson(0, 3)
    print("Maximum flow for the given graph is ", flow)

main()
