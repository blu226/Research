#NETWORK CLASS
from constants import *
from node import *
from message import *
from computeHarvesine import *
import os


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
    def try_forwarding_message_to_all(self,src_node, message, tau, LINK_EXISTS, specBW):

        for des_node in self.nodes:
            to_send = True

            if des_node != src_node:
                for mes in des_node.buf:
                    if mes.ID == message.ID:
                        to_send = False

                if to_send == True:
                    # if message.ID == 1:
                    #     print("SENDING: " + str(message.ID) + " at time " + str(tau) + " from " + str(
                    #         src_node.ID) + " to: " + str(des_node))
                    src_node.try_sending_message(des_node, message, tau, LINK_EXISTS, specBW)



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
                for i in range(num_mess_replicas):
                    new_mes = message(line_arr[0], line_arr[1], line_arr[2], line_arr[5], line_arr[4], i)
                    src = int(line_arr[1])
                    self.nodes[src].buf.append(new_mes)
                # print("New message: ", new_mes.ID, new_mes.src, new_mes.des)


#Function messages_delivered: deletes messages that have been delivered
    def messages_delivered(self):
        for node in self.nodes:
            for mes in node.buf:
                if int(mes.des) == int(node.ID):
                    f = open(Link_Exists_path + delivery_file_name, "a")
                    line = str(mes.ID) + "\t" + str(mes.src) + "\t" + str(mes.des) + "\t" + str(mes.genT) + "\t" + str(mes.last_sent)+ "\t" + str(mes.last_sent - mes.genT) + "\t" + str(mes.size) + "\t\t" + str(mes.parent) + "\t\t"  + str(mes.replica) + "\n"

                    f.write(line)
                    f.close()
                    node.buf.remove(mes)

    def all_messages(self):
        f = open(Link_Exists_path + notDelivered_file_name, "a")
        for node in self.nodes:
            # print("Node " + str(node.ID) + ": ")
            for mes in node.buf:
                line = str(mes.ID) + "\t" + str(mes.src) + "\t" + str(mes.des) + "\t" + str(mes.genT) + "\t" + str(mes.last_sent) + "\t" + str(mes.last_sent - mes.genT) + "\t" + str(mes.size) + "\t\t" + str(mes.parent) + "\t\t" + str(mes.replica) + "\n"
                # print(line)
                f.write(line)
        f.close()

    def remove_duplicate_messages(self, node):

        to_be_removed = []
        for i in range(0, len(node.buf) - 1):
            for j in range(i + 1, len(node.buf)):
                msg1 = node.buf[i]
                msg2 = node.buf[j]

                if msg1 in to_be_removed:
                    break

                if msg1.ID == msg2.ID:
                    if msg1.last_sent < msg2.last_sent:
                        to_be_removed.append(msg2)

                    else:
                        to_be_removed.append(msg1)

        for msg in to_be_removed:
            if msg.ID == debug_message:
                print(" Remove " + str(msg.ID) + " src " + str(msg.src) + " des: " + str(msg.des) + " curr: " + str(
                    node.ID))
            node.buf.remove(msg)



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
            # self.remove_duplicate_messages(node)
            for mes in node.buf:
                if mes.last_sent <= ts:
                    self.try_forwarding_message_to_all(node, mes, ts, LINK_EXISTS, specBW)
        #Handle messages that got delivered
        self.messages_delivered()
        #self.all_messages()

