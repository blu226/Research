#NETWORK CLASS
from constants import *
from node import *
from message import *
from computeHarvesine import *
import os

def find_delay(size, s, specBW, i, j, t):
    bw = specBW[i,j,s,t]
    return size/bw

#Function init: initialize node list and start time
class network(object):
    def __init__(self):
        self.nodes = []
        self.time = 0

#Function add_node: adds node to network
    def add_node(self, node):
        self.nodes.append(node)

#Function get_ID: gets ID for datamule, source, or destination from filename
    def get_ID(self, filename):
        if filename[1] == ".":
            return filename[0]
        else:
            return filename[:2]

# Function fill_network: create node objects for each datamule, source, and destination
    def fill_network(self):
        files = os.listdir(DataMule_path)
        nodeIDs = [int(self.get_ID(file)) for file in files]
        nodeIDs.sort()

        for i in range(len(nodeIDs)):
            node_ID = nodeIDs[i]
            node_curr = node(node_ID)
            self.add_node(node_curr)

    def euclideanDistance(coor1X, coor1Y, coor2X, coor2Y):
        return (math.sqrt((float(coor1X) - float(coor2X)) ** 2 + (float(coor1Y) - float(coor2Y)) ** 2))

        #Function send_message: sends message to all nodes in range
    def try_forwarding_message_to_all(self,src_node, message, t, LINK_EXISTS, specBW):

        real_des_node = self.nodes[message.des]
        #try to send to destination first
        if src_node.try_sending_message(real_des_node, message, t, LINK_EXISTS, specBW) == False:
        #if destination not in range, try to send message to node with the least delay
            delays = []

            for des_node in self.nodes:
                temp_delays = []

                if des_node != src_node:

                    for s in range(4):
                        delay = find_delay(message.size, s, specBW, src_node.ID, des_node.ID, t)
                        temp_delays.append(delay)

                    min_delay = min(temp_delays)

                    delays.append(min_delay)

            best_min_delay = min(delays)
            MF_des_node = self.nodes[delays.index(best_min_delay)]

            src_node.try_sending_message(MF_des_node, message, t, LINK_EXISTS, specBW)



#Function is_in_communication_range: checks if 2 nodes are within range of a certain spectrum
    def is_in_communication_range(self, node1, node2):
        dist = funHaversine(node1.coord[1], node1.coord[0], node2.coord[1], node2.coord[0])
        # dist = self.euclideanDistance(node1.coord[0], node1.coord[1], node2.coord[0], node2.coord[1])
        if dist < spectRange[0]:
            return True
        else:
            return False

#Function add_messages: adds messages to their source node at each tau
    def add_messages(self, time, lines):

        for line in lines:
            line_arr = line.strip().split()

            if int(line_arr[5]) == time:
                new_mes = message(line_arr[0], line_arr[1], line_arr[2], line_arr[5], line_arr[4])
                src = int(line_arr[1])
                self.nodes[src].buf.append(new_mes)
                # print("New message: ", new_mes.ID, new_mes.src, new_mes.des)


#Function messages_delivered: deletes messages that have been delivered
    def messages_delivered(self):
        for node in self.nodes:
            for mes in node.buf:
                if int(mes.des) == int(node.ID):
                    f = open(path_to_folder + delivery_file_name, "a")
                    line = str(mes.ID) + "\t" + str(mes.src) + "\t" + str(mes.des) + "\t" + str(mes.genT) + "\t" + str(mes.last_sent)+ "\t" + str(mes.last_sent - mes.genT) + "\t" + str(mes.size) + "\t\t" + str(mes.parent) +  "\n"

                    f.write(line)
                    f.close()
                    node.buf.remove(mes)

    def all_messages(self):
        f = open(path_to_folder + notDelivered_file_name, "a")
        for node in self.nodes:
            # print("Node " + str(node.ID) + ": ")
            for mes in node.buf:
                line = str(mes.ID) + "\t" + str(mes.src) + "\t" + str(mes.des) + "\t" + str(mes.genT) + "\t" + str(mes.last_sent) + "\t" + str(mes.last_sent - mes.genT) + "\t" + str(mes.size) + "\t\t" + str(mes.parent) +  "\n"
                # print(line)
                f.write(line)
        f.close()



    #Function network_GO: completes all tasks of a network in 1 tau
    def network_GO(self, ts, LINK_EXISTS, specBW, msg_lines):
        self.time = ts
        # Check if new messages were generated
        self.add_messages(ts, msg_lines)
        #Send all messages
        #For each node
        for i in range(len(self.nodes)):
            #For each message in this nodes buffer
            node = self.nodes[i]
            for mes in node.buf:
                if mes.last_sent <= ts and mes.des != node.ID:
                    self.try_forwarding_message_to_all(node, mes, ts, LINK_EXISTS, specBW)
        #Handle messages that got delivered
        self.messages_delivered()
        #self.all_messages()

