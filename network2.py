import random
import pickle
from node2 import *
from message2 import *
from constants import *

class Network(object):
    def __init__(self):
        self.nodes = []                 #list of nodes in network
        self.epoch_it = 0               #keeps track of current Tau
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

    def network_GO(self,t):                            #function that sends all messages at a given tau


        f = open(path_to_folder + "LLC_PATH.txt", "r")
        ADJ_T = pickle.load(open(path_to_folder + "ADJ_T.pkl", "rb"))
        ADJ_E = pickle.load(open(path_to_folder + "ADJ_E.pkl", "rb"))

        print(ADJ_E[3,0,0])
        for line in f:                                  #read each line from file to see if a new message needs to be generated
            line = line.strip()
            line = line.split(" ")

            if (int(line[2]) == self.epoch_it):         #if a new message needs to be generated at this time

                src = line[0]                           #get information from that line
                dst = line[1]
                T = line[2]
                size = line[3]
                i = 4
                # while line[i] is '' and i < len(line) -1:
                #     i +=1

                path = line[i:]
                name = self.message_num
                TTL = 5

                message = Message(src,dst,T,name,TTL,size,path, 0, 0)   #create the message
                curr = int(message.curr)

                self.nodes[curr].buf.append(message)                    #put the message in the source nodes buffer
                self.nodes[curr].buf_size += 1

                self.message_num += 1


        print("Network Status -- Time: ", self.epoch_it)            #console output for debugging
        # self.network_status()

        for i in range(len(self.nodes)):                #send all messages to their next hop
            node = self.nodes[i]
            print("\n For " +  node.name + " At time: " + str(t)  + " Buffer size: " + str(len(node.buf)))
            print("-------------------------------------- \n")
            for msg in node.buf:
                # print("Index: " + str(i) + " " + str(msg.ID))
                node.send_message( self, msg, t, ADJ_T, ADJ_E)

            print("-------------------------------------- ")

        self.epoch_it += 1
        f.close()

