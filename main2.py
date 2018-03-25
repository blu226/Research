from network2 import *
from node2 import *
from message2 import *


EPOCH_LEN = 2
NUM_NODES = 5                                                                           #number of nodes to put in network
NUM_SPECTRUMS = 4                                                                       #number of spectrums for each node
MAX_X = 100                                                                             #largest x-y coordinates in plane
MAX_Y = 100
T = 5

net = Network(EPOCH_LEN)
net.fill_network(NUM_NODES, MAX_X, MAX_Y)


for i in range(T):
    net.network_GO(i)


