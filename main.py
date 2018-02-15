from network import *
from node import *
from message import *
from helper_func import *
import threading
import time
import timeit
import random

#TEST MAIN

epoch_len = .5                                                                          #length in seconds of an epoch
num_nodes = 4                                                                           #number of nodes to put in network
num_spectrums = 4                                                                       #number of spectrums for each node
MAX_X = 100										#largest x-y coordinates in plane
MAX_Y = 100

adj = create_adj(num_nodes, num_spectrums)                                              #create adjacency matrix
adj2 = floyd_warshall(adj)
net = Network(epoch_len, adj)                                                           #create network object
net.fill_network(num_nodes, MAX_X, MAX_Y)						#add and place nodes in network
print("bandwidth")
print_3Dmatrix(adj)
net.energy_matrix(100)
print("energy consumed")
print_3Dmatrix(net.energy)
net.time_matrix(100)
print("time consumed")
print_3Dmatrix(net.time)
path_list = find_paths(0, num_nodes - 1,adj)                                            #find paths for messages from first node to last
n1 = net.nodes[0]                                                                       #grab first and last node in network
n2 = net.nodes[num_nodes - 1]


'''
net.epoch_log()                                                                         #start network log
m1 = Message(n1.name, n2.name, "m1", 10, path_list[0], 10)                              #create message 1
m2 = Message(n1.name, n2.name, "m2", 100, path_list[len(path_list)-1], 10)              #create message 2

#send messages
n1.send(m1, net)
n1.send(m2, net)
'''

