from network2 import *
from node2 import *
from message2 import *
from constants import *

                                                                                  #number of Taus

#initialize and fill network with nodes
net = Network()
net.fill_network(V, maxX, maxY)

#initialize output file
output_file = open("Delivery_Confirmation.txt", "w")
output_file.write("ID\tSRC\tDSTN\tStart\tEnd\t\tTotal Delay\t\tTotal Energy\n")
output_file.write("----------------------------------------------------\n")
output_file.close()

#run simulation
for i in range(T):
    net.network_GO(i)


