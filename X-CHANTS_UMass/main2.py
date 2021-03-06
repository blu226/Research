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

output_file2 = open(path_to_folder + consumedEnergyFile, 'w')
output_file2.write("Time\tEnergy\n")
output_file2.close()

path_to_LLC_arr = path_to_folder.split('/')
path_to_Day1_LLC = path_to_LLC_arr[0] + "/" + path_to_LLC_arr[1] + '/' + path_to_LLC_arr[2] + '/Day1/' + path_to_LLC_arr[4] + '/' + path_to_LLC_arr[5] + '/' + path_to_LLC_arr[6] + '/'

path_to_mess_arr = link_exists_folder.split('/')
path_to_mess = path_to_mess_arr[0] + '/' + path_to_mess_arr[1] + '/' + path_to_mess_arr[2] + '/Day1/generated_messages.txt'

with open(path_to_Day1_LLC + "LLC_PATH.txt", "r") as fp:
    path_lines = fp.readlines()[1:]


with open(path_to_Day1_LLC + "LLC_Spectrum.txt", "r") as fs:
    spec_lines = fs.readlines()[1:]

with open(generated_messages_file, "r") as fg:
    msg_lines = fg.readlines()[1:]

specBW = pickle.load(open("../Bands_UMass" + str(max_nodes) + "/" +  path_to_LLC_arr[2] +"/" + path_to_LLC_arr[3] + "/specBW.pkl", "rb"))
LINK_EXISTS = pickle.load(open("../Bands_UMass" + str(max_nodes) + "/" + path_to_LLC_arr[2] + "/" + path_to_LLC_arr[3] + "/LINK_EXISTS.pkl", "rb"))

#run simulation
print("Starting Simulation.")
for t in range(0, T, tau):
    net.network_GO(t, specBW, path_lines, spec_lines, msg_lines, LINK_EXISTS)


