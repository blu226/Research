import random
import threading
from node2 import *
from message2 import *

class Network(object):
    def __init__(self, epoch_len):
        self.nodes = []
        self.epoch_len = epoch_len
        self.epoch_it = 0
        self.message_num = 0

    def add_node(self, node):                                                           #add node to network
        node.netID = len(self.nodes)
        self.nodes.append(node)

    def fill_network(self, num_nodes, MAX_X, MAX_Y):                                    #quickly fill network and randomly place nodes
        for i in range(num_nodes):                                                      #create and add nodes to network
            ide = "Node" + str(i)
            x = random.randrange(0, MAX_X, 1)
            y = random.randrange(0, MAX_Y, 1)
            node = Node(ide)
            node.place(x, y)
            self.add_node(node)

    def network_status(self):
        for i in range(len(self.nodes)):
            print(self.nodes[i].name)
            print(self.nodes[i].print_buf())
            print()

    def network_GO(self,t):

        print("Network Status -- Time: ", self.epoch_it)
        self.network_status()
        f = open("path.txt", "r")

        for line in f:

            line = line.strip()
            line = line.split(" ")

            if (int(line[2]) == self.epoch_it):

                src = line[0]
                dst = line[1]
                T = line[2]
                size = line[3]
                path = line[4:]
                name = self.message_num
                TTL = 5
                message = Message(src,dst,T,name,TTL,size,path)
                curr = int(message.curr)
                print(message.ID)
                self.nodes[curr].buf.append(message)

                self.message_num += 1

        for i in range(len(self.nodes)):
            node = self.nodes[i]
            buf_len = len(node.buf)
            for j in range(buf_len - 1):
#                print("Buffer length is ", buf_len)
                print("number of nodes ", len(self.nodes))
                message = self.nodes[i].buf[j]
#                node.send_message(message,self)

        self.epoch_it += 1
        f.close()

