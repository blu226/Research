from network2 import *
from node2 import *
from message2 import *

NUM_NODES = 5                                                                           #number of nodes to put in network
NUM_SPECTRUMS = 4                                                                       #number of spectrums for each node
MAX_X = 100                                                                             #largest x-y coordinates in plane
MAX_Y = 100
T = 10                                                                                  #number of Taus

#initialize and fill network with nodes
net = Network()
net.fill_network(NUM_NODES, MAX_X, MAX_Y)

#initialize output file
output_file = open("Delivery_Confirmation.txt", "w")
output_file.write("ID\tSRC\tDSTN\tStart\tEnd\t\tTotal Delay\t\tTotal Energy\n")
output_file.write("----------------------------------------------------\n")
output_file.close()

#run simulation
for i in range(T):
    net.network_GO(i)


