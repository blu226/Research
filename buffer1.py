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
        self.name = name								#Node ID or name
        self.buf = []                                   				#Node message buffer
        self.netID = 0									#ID of node in network class

    def send_message(self, message):							#send message
        nodes = net.nodes
        path = message.path								#find path for message to follow
        for i in range(len(path)):							#for each node in the path
            cur = path[i][0]
            next = path[i][1]
            spec = path[i][2]
            print("Hop: ", i)
            time.sleep(1)
            if(i == 0):									#if message is at sender
                nodes[next].buf.append(message)						#copy message to next node's buf
                message.curr = nodes[next].name						#update messages's current node status
            elif(i < len(path) - 1):							#if message is not at sender
                nodes[next].buf.append(message)						#copy message to next node's buf
                message.curr = nodes[next].name						#update message's current node status
                nodes[cur].buf.remove(message)						#remove message from previous node's buf
            if i != len(path) - 1:
                message.ttl -= (message.size / net.adj[cur][next][spec]) 		#subtract time taken from ttl
            else:
                if i == 0:
                    nodes[next].buf.remove(message)
                else:
                    nodes[cur].buf.remove(message)
        print("message sent")
#--------------------------------------------------------------------------------------------------------------------------------

class Message(object):										#Message Object
    def __init__(self, src, des, name, ttl, path, size):
        self.src = src									#message source node
        self.des = des									#message destination node
        self.ttl = ttl									#message ttl
        self.name = name								#message name
        self.curr = src									#current node message is located at
        self.path = path								#path for message to follow
        self.size = size
#--------------------------------------------------------------------------------------------------------------------------------
#OTHER FUNCTIONS

def print_networkmap(adj):								#function to clearly show the details of the
    print("Network Map")								#the network
    for i in range(len(adj)):
        print("Node ", i, ":")
        for j in range(len(adj[i])):
            print("\t node ", j)
            for k in range(len(adj[i][j])):
                print("\t\t -Spectrum ", k, ": ", adj[i][j][k])

def create_adj(nodes, spectrums):							#function to randomly generate 3D adj matrix
    max_weight = 20
    adj = [[[random.randrange(5,max_weight,5) for x in range(spectrums)] for y in range(nodes)] for z in range(nodes)]
    for i in range(len(adj)):
        for j in range(spectrums):
            adj[i][i][j] = 0
    for i in range(len(adj)):
        for j in range(len(adj)):
            for z in range(spectrums):
                adj[j][i][z] = adj[i][j][z]
    for i in range((2*nodes*spectrums)):
        x = random.randrange(0,nodes,1)
        y = random.randrange(0,nodes,1)
        for j in range(spectrums):
            adj[x][y][j] = 0
            adj[y][x][j] = 0
    return adj

def dfs(F, s, t, matrix):                                                     	#DFS function [flow matrix, source, sink]
    num_spectrums = len(matrix[0][0])
    stack = [s]                                                             	#create stack to keep track of where to go
    paths = {s: []}                                                         	#create path dict to keep track of paths
    if s == t:                                                              	#checks if source = destination
        return paths[s]
    while stack:                                                            	#while loop to find paths while stack isn't empty
        cur = stack.pop()                                                   	#create variable for current node being traversed
        for i in range(len(F)):
            for j in range(num_spectrums):
                if (matrix[cur][i][j]-F[cur][i][j] > 0) and i not in paths:      	#check if there is a path
                    paths[i] = paths[cur] + [(cur,i,j)]                           	#add path to dict
                    if i == t:                                                  	#check if sink node has been reached
                        return paths[i]
                    stack.append(i)                                             	#add node with edge to stack to be traversed
    return "None"

def ford_fulkerson(s, t, matrix):                                               #Ford and Fulkerson function [source, sink]
    paths = []
    F = [[[0]*(len(matrix)) for i in range(len(matrix))] for j in range(len(matrix))]                        	#create identical sized graph to keep track of flow
    path = dfs(F, s, t, matrix)                                                 	#find first path using DFS
    while path != "None":                                                  	#loop while a path still exists
        paths.append(path)
        flow = min(matrix[u][v][i] - F[u][v][i] for u,v,i in path)		#find flow value
        for u,v,i in path:                    		                #update flow matrix
            F[u][v][i] += flow
            F[v][u][i] -= flow
        path = dfs(F, s, t, matrix)   		                                #find new path
    max_flow = sum(F[s][i][0] for i in range(len(matrix)))			#maximum flow
    return paths								#return paths found for max flow

def find_paths(s, t, adj):
    hops = []
    paths = ford_fulkerson(s, t, adj)
    for i in range(len(paths)):
        temp = []
        for x,y,z in paths[i]:
            src = x
            dst = y
            spec = z
            hop = [src, dst, spec]
            temp.append(hop)
        hops.append(temp)
    return hops
#------------------------------------------------------------------------------------------------------------------------------------
#TEST MAIN

epoch_len = .5
num_nodes = 10
num_spectrums = 3
adj = create_adj(num_nodes, num_spectrums)
path_list = find_paths(0,9,adj)
print(path_list)
print_networkmap(adj)
net = Network(epoch_len, adj)
for i in range(num_nodes):
    ide = "Node" + str(i)
    node = Node(ide)
    net.add_node(node)
n1 = net.nodes[0]
n2 = net.nodes[num_nodes - 1]
net.epoch_log()
m1 = Message(n1.name, n2.name, "m1", 10, path_list[0], 10)
m2 = Message(n1.name, n2.name, "m2", 100, path_list[1], 10)

#send messages
t1 = threading.Thread(target = n1.send_message, args = (m1,))
t2 = threading.Thread(target = n1.send_message, args = (m2,))
t2.start()
t1.start()
t1.join()
t2.join()

