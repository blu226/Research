import random
import pickle
from node2 import *
from message2 import *
from constants import *

class Network(object):
    def __init__(self):
        self.nodes = []                 #list of nodes in network
        # self.epoch_it = 0               #keeps track of current Tau
        self.message_num = 0            #keeps track of available message ID numbers

    def add_node(self, node):           #add node to network
        node.netID = len(self.nodes)
        self.nodes.append(node)

    def fill_network(self, num_nodes):          #quickly fill network and randomly place nodes
        for i in range(num_nodes):                            #create and add nodes to network
            ide = str(i)
            node = Node(ide)
            node.load_pkl()
            self.add_node(node)

    def find_avg_energy_consumption(self, time):
        total_energy = 0

        for node in self.nodes:
            total_energy += node.energy

        avg_energy = total_energy / V

        f = open(path_to_folder + consumedEnergyFile, 'a')
        f.write(str(time) + "\t" + str(avg_energy) + "\n")
        f.close()

    def network_status(self):                          #console output for debugging (prints all messages in each nodes buffer)
        for i in range(len(self.nodes)):
            self.nodes[i].print_buf()
            print(" ")

    #Get message size, path, spectrum info for the current message
    def get_message_info(self, path_lines, spec_lines, src, des, t, size):
        # print("Inside: ", src, des, t)
        path = []
        band = []
        for ind in range(len(path_lines)):  # read each line from file to see if a new message needs to be generated
            path_line = path_lines[ind].strip()
            path_line_arr = path_line.split("\t")

            spec_line = spec_lines[ind].strip()
            spec_line_arr = spec_line.split("\t")

            if int(path_line_arr[2]) == int(t) and int(path_line_arr[0]) == int(src) and int(path_line_arr[1]) == int(
                    des) and int(path_line_arr[3]) == int(size):
                # print (path_line_arr)
                path = path_line_arr[5: len(path_line_arr) - 1]
                band = spec_line_arr[5:]

        # print (path, band)
        return path, band


    def network_GO(self, t, specBW, path_lines, spec_lines, msg_lines):                            #function that sends all messages at a given tau

        if t % 15 == 0 or t == 119:
            self.find_avg_energy_consumption(t)

        for msg_id in range(len(msg_lines)):
            msg_line = msg_lines[msg_id].strip()
            msg_line_arr = msg_line.split("\t")

            if (int(msg_line_arr[5]) == t):  # if a new message needs to be generated at this time
                # print(msg_line_arr)
                id = msg_line_arr[0]
                src = msg_line_arr[1]  # get information from that line
                des = msg_line_arr[2]
                TTL = msg_line_arr[3]
                size = msg_line_arr[4]

                path, band = self.get_message_info(path_lines, spec_lines, src, des, t, size)

                message = Message(src, des, t, id, TTL, size, path, band, 0, 0, 0)  # create the message
                curr = int(message.curr)

                # If a path exists for this message
                if len(message.path) > 0:
                    # if len(message.path) + t >= 90:
                    #     print("Error 1: ", " ID ", id, " src: ", src, " des: ", des, " t ", t)

                    self.nodes[curr].buf.append(message)  # put the message in the source nodes buffer
                    self.nodes[curr].buf_size += 1
                    self.message_num += 1

                # else:
                #     print("Error 2: ", " ID ", id, " src: ", src, " des: ", des, " t ", t)
        # print("Network Status -- Time: ", t)            #console output for debugging
        # self.network_status()

        for i in range(len(self.nodes)):                #send all messages to their next hop
            node = self.nodes[i]
            isVisited = len(node.buf) #Get the initial buffer size

            while len(node.buf) > 0 and isVisited > 0:
                msg = node.buf[ isVisited - 1]
                node.send_message( self, msg, t, specBW)
                # the message gets deleted from the current node, and buffer gets shrinked
                # isVisited is to get to the end of the node buffer even if it is not empty
                isVisited -= 1





