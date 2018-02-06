#Author: Brian Luciano

import time
import timeit
import threading
import random

#-------------------------------------------------------------------------------------------------------------------------------------
#CLASSES
class Network(object):										#Network Object
    def __init__(self, epoch_len, adj):
        self.nodes = []									#nodes connected to network
        self.epoch_len = epoch_len							#time length of 1 epoch
        self.epoch_it = 0								#number of epochs that have passed
        self.adj = adj									#adjacency matrix

    def add_node(self, node):								#add node to network
        node.netID = len(self.nodes)
        self.nodes.append(node)

    def epoch_log(self):                                                                #list each message in transit at each epoch
        t = threading.Timer(self.epoch_len, self.epoch_log).start()                     #starts timer to replay code every epoch_len secs
        f = open("test.txt", 'a', encoding = 'utf-8')                                   #open file to write to
        self.epoch_it += 1                                                              #increase number of epochs that have passed by  1
        f.write("\n----------------------\n")
        f.write("EPOCH ")
        f.write(str(self.epoch_it))                                                     #Write to file the current epoch number
        f.write("\n----------------------\n")
        for i in range(len(self.nodes)):                                                #For each node within the network if a
            cur_node = self.nodes[i]                                                    # node has a message in its buffer then
            if len(cur_node.buf) > 0:                                                   # write the info to the file under the
                for j in range(len(cur_node.buf)):                                      # current epoch
                    f.write("|ID: ")
                    f.write(cur_node.buf[j].name)
                    f.write("\n")
                    f.write("|SRC: ")
                    f.write(cur_node.buf[j].src)
                    f.write("\n")
                    f.write("|DES: ")
                    f.write(cur_node.buf[j].des)
                    f.write("\n")
                    f.write("|TTL: ")
                    f.write(str(cur_node.buf[j].ttl))
                    f.write("\n")
                    f.write("|Current Node: ")
                    f.write(cur_node.buf[j].curr)
                    f.write("\n\n")
        f.close()

#---------------------------------------------------------------------------------------------------------------------------
class Node(object):									#Node Object
    def __init__(self, name):
        self.name = name								#Node ID or name (string)
        self.buf = []                                   				#Node message buffer
        self.netID = 0									#ID of node in network class (int)

    def send_message(self, message):							#send message
        nodes = net.nodes
        path = message.path								#find path for message to follow
        for i in range(len(path)):							#for each node in the path
            cur = path[i][0]
            next = path[i][1]
            spec = path[i][2]
            print("Hop: ", i)								#print hop number (for debugging purposes)
            time.sleep(1)								#wait 1 sec so messages dont move faster then epoch_len
            if(i == 0):									#if message is at sender
                nodes[next].buf.append(message)						#copy message to next node's buf
                message.curr = nodes[next].name						#update messages's current node status
            elif(i < len(path) - 1):							#if message is not at sender
                nodes[next].buf.append(message)						#copy message to next node's buf
                message.curr = nodes[next].name						#update message's current node status
                nodes[cur].buf.remove(message)						#remove message from previous node's buf
            if i != len(path) - 1:							#if message isn't at destination
                message.ttl -= (message.size / net.adj[cur][next][spec]) 		#subtract time taken from ttl (msg size / bandwidth)
            else:									#if message is at destination
                if i == 0:								#and there was only 1 hop
                    nodes[next].buf.remove(message)					#remove message from destination buffer
                else:									#if message is at destination and took > 1 hop
                    nodes[cur].buf.remove(message)					#remove message from destination buffer
        print("message sent")								#print message sent (for debugging purposes)
#--------------------------------------------------------------------------------------------------------------------------------

class Message(object):										#Message Object
    def __init__(self, src, des, name, ttl, path, size):
        self.src = src									#message source node
        self.des = des									#message destination node
        self.ttl = ttl									#message ttl
        self.name = name								#message name
        self.curr = src									#current node message is located at
        self.path = path								#path for message to follow
        self.size = size								#size of message
#--------------------------------------------------------------------------------------------------------------------------------
#OTHER FUNCTIONS
def print_3Dmatrix(adj):
    for i in range(len(adj)):
        for j in range(len(adj)):
            print(adj[i][j], " ", end="")
        print()

def print_networkmap(adj):								#function to clearly show the details of the
    print("Network Map")								#the nodes in the network and the weights
    for i in range(len(adj)):								#between each node
        print("Node ", i, ":")
        for j in range(len(adj[i])):
            print("\t node ", j)
            for k in range(len(adj[i][j])):
                print("\t\t -Spectrum ", k, ": ", adj[i][j][k])

def create_adj(nodes, spectrums):							#function to randomly generate 3D adj matrix
    max_weight = 20									#set a maximum weight for edges
    min_weight = 5									#set a min weight > 0 for edges
    step = 5										#step interval for random numbers
    adj = [[[random.randrange(min_weight, max_weight, step) for x in range(spectrums)] for y in range(nodes)] for z in range(nodes)] #creates matrix with random numbers specified by max_weight, min_weight, and step
    for i in range(len(adj)):								#set 0 for "edges" to the same node
        for j in range(spectrums):
            adj[i][i][j] = 0
    return adj
'''
    for i in range(len(adj)):								#OPTIONAL for loop to make edges bidirectional
        for j in range(len(adj)):							#in a way such that the weight(i, j) = weight(j, i)
            for z in range(spectrums):
                adj[j][i][z] = adj[i][j][z]
    for i in range((10*nodes*spectrums)):						#OPTIONAL for loop to randomly place edges with
        x = random.randrange(0,nodes,1)							#a weight of 0 into the adj matrix
        y = random.randrange(0,nodes,1)
        for j in range(spectrums):
            adj[x][y][j] = 0
            adj[y][x][j] = 0
'''
#    return adj										#return a 3D list

def dfs(F, s, t, matrix):                                                     		#DFS function [flow matrix, source, sink]
    num_spectrums = len(matrix[0][0])
    stack = [s]                                                             		#create stack to keep track of where to go
    paths = {s: []}                                                         		#create path dict to keep track of paths
    if s == t:                                                              		#checks if source = destination
        return paths[s]
    while stack:                                                            		#while loop to find paths while stack isn't empty
        cur = stack.pop()                                                   		#create variable for current node being traversed
        for i in range(len(F)):
            for j in range(num_spectrums):
                if (matrix[cur][i][j]-F[cur][i][j] > 0) and i not in paths:     	#check if there is a path
                    paths[i] = paths[cur] + [(cur,i,j)]                         	#add path to dict
                    if i == t:                                                  	#check if sink node has been reached
                        return paths[i]							#if sink has been reached return path found
                    stack.append(i)                                             	#add node with edge to stack to be traversed
    return "None"

def ford_fulkerson(s, t, matrix):                                               	#Ford and Fulkerson function [source, sink, matrix]
    paths = []
    F = [[[0]*(len(matrix[0][0])) for i in range(len(matrix))] for j in range(len(matrix))]   #create identical sized graph to keep track of flow
    path = dfs(F, s, t, matrix)                                                 	#find first path using DFS
    while path != "None":                                                  		#loop while a path still exists
        paths.append(path)
        flow = min(matrix[u][v][i] - F[u][v][i] for u,v,i in path)			#find flow value
        for u,v,i in path:                    		                		#update flow matrix
            F[u][v][i] += flow
            F[v][u][i] -= flow
        path = dfs(F, s, t, matrix)   		                                	#find new path
    max_flow = sum(F[s][i][0] for i in range(len(matrix)))				#maximum flow
    return paths									#return paths found for max flow

def find_paths(s, t, adj):								#function to find maximum flow paths
    hops = []
    paths = ford_fulkerson(s, t, adj)							#find max flow paths
    for i in range(len(paths)):								#for each of the paths in the max flow
        temp = []									#create temp list to store hop data
        for x,y,z in paths[i]:								#for each hop in a path
            src = x
            dst = y
            spec = z									#store each hop as a list containing
            hop = [src, dst, spec]							#[source, destination/next hop, spectrum]
            temp.append(hop)								#add hop to path list
        hops.append(temp)								#add path to paths list
    return hops										#return list of paths

def floyd_warshall(adj):								#Floyd-Warshall function
    length = len(adj)
    num_spectrums = len(adj[0][0])
    inf = 1000										#variable to simulate infinity
    dist = [[[inf]*num_spectrums for i in range(length)] for j in range(length)] 	#create a distance matrix the same size
    for i in range(length):								#as adj and add edges if they exist
        for j in range(length):
            for s in range(num_spectrums):
                if (adj[i][j][s] != 0):
                    dist[i][j][s] = adj[i][j][s]
    for k in range(length):								#for each intermediate node k between i and j
        for i in range(length):								#check to see the path from i to k to j is
            for j in range(length):							#shorter than the path from i to j
                for s in range(num_spectrums):
                    if (dist[i][j][s] > (dist[i][k][s] + dist[k][j][s]) and (i != j)):	#if so and i != j
                        dist[i][j][s] = dist[i][k][s] + dist[k][j][s]			#update the distance matrix
    for i in range(length):								#set the weight from a node to itself as 0
        for j in range(length):
            if i == j:
                for s in range(num_spectrums):
                    dist[i][j][s] = 0
    return dist


#------------------------------------------------------------------------------------------------------------------------------------
#TEST MAIN

epoch_len = .5										#length in seconds of an epoch
num_nodes = 4										#number of nodes to put in network
num_spectrums = 2									#number of spectrums for each node
adj = create_adj(num_nodes, num_spectrums)						#create adjacency matrix
adj2 = floyd_warshall(adj)
net = Network(epoch_len, adj)								#create network object
for i in range(num_nodes):								#create and add nodes to network
    ide = "Node" + str(i)
    node = Node(ide)
    net.add_node(node)
path_list = find_paths(0, num_nodes - 1,adj) 						#find paths for messages from first node to last
n1 = net.nodes[0]									#grab first and last node in network
n2 = net.nodes[num_nodes - 1]
net.epoch_log()										#start network log
m1 = Message(n1.name, n2.name, "m1", 10, path_list[0], 10)				#create message 1
m2 = Message(n1.name, n2.name, "m2", 100, path_list[len(path_list)-1], 10)		#create message 2

#send messages
t1 = threading.Thread(target = n1.send_message, args = (m1,))
t2 = threading.Thread(target = n1.send_message, args = (m2,))
t2.start()
t1.start()
t1.join()
t2.join()

print_3Dmatrix(adj)
print("NEXT")
print_3Dmatrix(adj2)
