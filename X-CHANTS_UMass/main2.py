from network3 import *
from node2 import *
from message2 import *
from constants import *

                                                                                  #number of Taus

#initialize and fill network with nodes
net = Network()
net.fill_network(V)

#initialize output file
output_file = open(path_to_folder + delivery_file_name, "w")
output_file.write("ID\ts\td\tts\tte\tLLC\tELC\n")
output_file.write("----------------------------------------------------\n")
output_file.close()

with open(path_to_folder + "LLC_PATH.txt", "r") as fp:
    path_lines = fp.readlines()[1:]


with open(path_to_folder + "LLC_Spectrum.txt", "r") as fs:
    spec_lines = fs.readlines()[1:]

with open(generated_message_file, "r") as fg:
    msg_lines = fg.readlines()[1:]

specBW = pickle.load(open(link_exists_folder + "specBW.pkl", "rb"))

#run simulation
print("Starting Simulation.")
for t in range(0, T, tau):

    net.network_GO(t, specBW, path_lines, spec_lines, msg_lines)


