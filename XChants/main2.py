from network3 import *
from node2 import *
from message2 import *
from constants import *

                                                                                  #number of Taus

#initialize and fill network with nodes
net = Network()
net.fill_network(V, maxX, maxY)

#initialize output file
output_file = open(path_to_folder + delivery_file_name, "w")
output_file.write("ID\ts\td\tts\tte\tm\tLLC\tELC\n")
output_file.write("----------------------------------------------------\n")
output_file.close()

day1_link_exists = link_exists_folder.split("/")
specBW = pickle.load(open("../" + day1_link_exists[1] + "/" + day1_link_exists[2] + "/Day1/specBW.pkl", "rb"))

day1_folder_path = path_to_folder.split("/")
with open("../" + day1_folder_path[1] + "/" + day1_folder_path[2] + "/Day1/" + day1_folder_path[4] + "/LLC_PATH.txt", "r") as fp:
    path_lines = fp.readlines()[1:]


with open("../" + day1_folder_path[1] +"/" + day1_folder_path[2] + "/Day1/" + day1_folder_path[4] + "/LLC_Spectrum.txt", "r") as fs:
    spec_lines = fs.readlines()[1:]

message_path_file = "../Bands" + str(max_nodes) + "/" + link_exists_folder.split("/")[2] + "/Day1/generated_messages.txt"
print("Message file: ", message_path_file)

with open(message_path_file, "r") as fg:
    msg_lines = fg.readlines()[1:]
    print(msg_lines[0])

#run simulation
for t in range(0, T, tau):
    # print("Time: ", t)
    net.network_GO(t, specBW, path_lines, spec_lines, msg_lines)


