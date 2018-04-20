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

    def fill_network(self, num_nodes, MAX_X, MAX_Y):          #quickly fill network and randomly place nodes
        for i in range(num_nodes):                            #create and add nodes to network
            ide = "Node " + str(i)
            x = random.randrange(0, MAX_X, 1)
            y = random.randrange(0, MAX_Y, 1)
            node = Node(ide)
            node.place(x, y)
            self.add_node(node)

    def network_status(self):                          #console output for debugging (prints all messages in each nodes buffer)
        for i in range(len(self.nodes)):
            self.nodes[i].print_buf()
            print(" ")

    #Get message size, path, spectrum info for the current message
    def get_message_info(self, path_lines, spec_lines, src, des, t):
        # print("Inside: ", src, des, t)
        path = []
        band = []
        for ind in range(len(path_lines)):  # read each line from file to see if a new message needs to be generated
            path_line = path_lines[ind].strip()
            path_line_arr = path_line.split("\t")

            spec_line = spec_lines[ind].strip()
            spec_line_arr = spec_line.split("\t")

            if int(path_line_arr[2]) == int(t) and int(path_line_arr[0]) == int(src) and int(path_line_arr[1]) == int(des):
                # print (path_line_arr)
                path = path_line_arr[4: len(path_line_arr) - 1]
                band = spec_line_arr[4:]

        # print (path, band)
        return path, band


    def network_GO(self, t):                            #function that sends all messages at a given tau

        with open(path_to_folder + "LLC_PATH.txt", "r") as fp:
            path_lines = fp.readlines()[1:]
        fp.close()

        with open(path_to_folder + "LLC_Spectrum.txt", "r") as fs:
            spec_lines = fs.readlines()[1:]
        fs.close()

        with open ("generated_messages.txt", "r") as fg:
            msg_lines = fg.readlines()[1:]

        for msg_id in range(len(msg_lines)):
            msg_line =  msg_lines[msg_id].strip()
            msg_line_arr = msg_line.split("\t")


            if (int(msg_line_arr[5]) == t ):         #if a new message needs to be generated at this time
                # print(msg_line_arr)
                id = msg_line_arr[0]
                src = msg_line_arr[1]                           #get information from that line
                des = msg_line_arr[2]
                TTL = msg_line_arr[3]
                size = msg_line_arr[4]

                path, band = self.get_message_info(path_lines, spec_lines, src, des, t)

                message = Message(src, des, t, id, TTL, size, path, band, 0, 0, 0)   #create the message
                curr = int(message.curr)

                #If a path exists for this message
                if len(message.path) > 0:
                    self.nodes[curr].buf.append(message)      #put the message in the source nodes buffer
                    self.nodes[curr].buf_size += 1
                    self.message_num += 1


        # print("Network Status -- Time: ", t)            #console output for debugging
        # self.network_status()

        for i in range(len(self.nodes)):                #send all messages to their next hop
            node = self.nodes[i]
            print("\n For " +  node.name + " At time: " + str(t)  + " Buffer size: " + str(len(node.buf)))
            # print("Current messages at node : ", node.name)
            # for msg in node.buf:
            #     print(msg.ID, "-", msg.path, end= " ")

            isVisited = len(node.buf) #Get the initial buffer size
            print("\n--------------------------------------")

            while len(node.buf) > 0 and isVisited > 0:
                msg = node.buf[isVisited - 1]
                # print("Buffer: ", [msg.ID for msg in node.buf])
                print("\nMsg: " + str(msg.ID), " src " + str(msg.src), " des: " + str(msg.des), " genT: " + str(msg.T), "path: ", msg.path )
                node.send_message( self, msg, t)
                isVisited -= 1

            print("-------------------------------------- ")

        # self.epoch_it += 1


