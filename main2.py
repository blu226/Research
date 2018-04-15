from network2 import *
from node2 import *
from message2 import *
from constants import *

                                                                                  #number of Taus

#initialize and fill network with nodes
net = Network()
net.fill_network(V, maxX, maxY)

#initialize output file
output_file = open(path_to_folder + "LLC_delivery_confirmation.txt", "w")
output_file.write("ID\tSRC\tDSTN\tStart\tEnd\t\tTotal Delay\t\tTotal Energy\n")
output_file.write("----------------------------------------------------\n")
output_file.close()

#run simulation
for t in range(0, T, tau):
    net.network_GO(t)


