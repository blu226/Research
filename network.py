#Author: Brian Luciano

from node import *
import time
import timeit
import threading
import random
from helper_func import *
#-------------------------------------------------------------------------------------------------------------------------------------
#CLASSES
class Network(object):                                                                          #Network Object
    def __init__(self, epoch_len, adj):
        self.nodes = []                                                                 #nodes connected to network
        self.epoch_len = epoch_len                                                      #time length of 1 epoch
        self.epoch_it = 0                                                               #number of epochs that have passed
        self.adj = adj                                                                  #matrix to hold the bandwidth of each spectrum between 2 nodes
        self.dist = []									#matrix to hold the distances between each node
        self.energy = []								#matrix to hold energy consumed from one node to the next
        self.time = []									#matrix to hold time consumed from one node to another based on spectrum
        self.W = []									#W matrix
        self.P = []									#P matrix

    def add_node(self, node):                                                           #add node to network
        node.netID = len(self.nodes)
        self.nodes.append(node)

    def fill_network(self, num_nodes, MAX_X, MAX_Y):					#quickly fill network and randomly place nodes
        for i in range(num_nodes):                                                      #create and add nodes to network
            ide = "Node" + str(i)
            x = random.randrange(0, MAX_X, 1)
            y = random.randrange(0, MAX_Y, 1)
            node = Node(ide)
            node.place(x, y)
            self.add_node(node)

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

    def dist_matrix(self):
        length = len(self.nodes)
        dist = [[0 for i in range(length)] for j in range(length)]
        for i in range(length):
            for j in range(length):
                dist[i][j] = distance(self.nodes[i], self.nodes[j])
        self.dist = dist

    def energy_matrix(self, size):
        p = [1 for i in range(len(self.adj[0][0]))]					#P value for each spectrum
        length = len(self.nodes)
        energy = [[[-1 for i in range(len(self.adj[0][0]))] for i in range(length)] for j in range(length)]	#initialize energy matrix with -1 default
        for i in range(length):
            for j in range(length):
                for s in range(len(self.adj[0][0])):
                    if (self.adj[i][j][s] != 0):					#if there exists a link
                        energy[i][j][s] = round((p[s] * (size / self.adj[i][j][s])), 2)		#calculate the energy cost
        self.energy = energy								#store matrix in network object

    def time_matrix(self, size):
        length = len(self.nodes)
        time = [[[-1 for s in range(len(self.adj[0][0]))] for i in range(length)] for j in range(length)]
        for i in range(length):
            for j in range(length):
                for s in range(len(self.adj[0][0])):
                    if (self.adj[i][j][s] != 0):					#if a link exists
                        time[i][j][s] =round((size / self.adj[i][j][s]), 2)			#calculate time consumed
        self.time = time								#store matrix in network object

    def initializeADJ_MAT(V, T, ADJ_T, ADJ_E):

        W = np.full((V, V, T), np.inf)  # Adjacency matrix with T
        P = np.full((V, V, T), -1)  # Path tracking matrix

        for u in range(V):
            for v in range(V):
                minECost = math.inf
                isValidPath = False

                for t in range(0, T):
                    if u == v:
                        W[u][v][t] = 0
                        P[u][v][t] = -1

                    if u != v and ADJ_T[u][v] == t and minECost > ADJ_E[u][v]:
                        isValidPath = True
                        W[u][v][t]  = ADJ_E[u][v]
                        minECost    = W[u][v][t]
                        P[u][v][t]  = u

                    if u != v and isValidPath == False:
                        W[u][v][t] = math.inf
                        P[u][v][t] = -1

                    if t > 0 and W[u][v][t] > W[u][v][t-1]:
                        W[u][v][t] = W[u][v][t-1]
                        minECost   = W[u][v][t-1]
                        P[u][v][t] = u

        self.W = W
        self.P = P
