import pickle
import math
from computeHarvesine import *
from constants import *
from STB_help import *

class Node(object):                                                                     #Node Object
    def __init__(self, name):
        self.name = name                                                                #Node ID or name (string)
        self.buf = []                                                                   #Node message buffer
        self.coord = [0, 0]
        self.buf_size = 0

    def place(self, x, y):                                                              #place node on x-y plane
        self.coord[0] = x
        self.coord[1] = y

    def print_buf(self):
        # print(str(self.name) +  " Buffer ")
        if len(self.buf) == 0:
            print(">>>>>>>>>>>>> No messages")

        for i in range(len(self.buf)):
            message = self.buf[i].ID
            print("Message ID: " + str(message))

    def get_attributes(self, curr, t, s):
        curr_coorX = -1
        curr_coorY  = -1

        with open(validate_data_directory + str(curr) + ".txt", "r") as fc:
            lines = fc.readlines()[1:]
            for line in lines:
                curr_line_arr = line.strip().split()
                #print(str(curr_line_arr))
                if str(int(float(curr_line_arr[0]))) == str(t):

                    curr_coorX = curr_line_arr[2]
                    curr_coorY = curr_line_arr[3]

                    if s < 0:
                        print("S can not be less than 0", s)

                    # else:
                    #     curr_bandwidth = curr_line_arr[s + 2]

        return curr_coorX, curr_coorY

    def is_in_communication_range(self, curr, next, t, s):
        curr_coorX, curr_coorY = self.get_attributes(curr, t + StartTime, s)
        next_coorX, next_coorY = self.get_attributes(next, t + StartTime, s)

       # print(curr_coorX, curr_coorY, next_coorX, next_coorY, s)
        # print("Dist: ", euclideanDistance(curr_coorX, curr_coorY, next_coorX, next_coorY), s, spectRange[s])
        if curr_coorX == -1 or next_coorX == -1:
            return False

        elif funHaversine(float(curr_coorY),float(curr_coorX), float(next_coorY), float(next_coorX)) <= spectRange[s]:
            #print("t: " + str(t) + " X: " + str(curr_coorX) + " Y: " + str(curr_coorY))
            return True

        return False

    def send_message(self, net, message, t):

        # This file is equivalent to LLC (for LLC path) and TLLC (for TLEC path)
        ADJ_T = pickle.load(open(path_to_folder + "ADJ_T.pkl", "rb"))

        # This file is equivalent to ELC (for LLC path) and TLEC (for TLEC path)
        ADJ_E = pickle.load(open(path_to_folder + "ADJ_E.pkl", "rb"))

        nodes = net.nodes

        # print("Message ID: " + str(message.ID) + " path: " + str(message.path))         #console output for debugging

        if len(message.path) > 0 and '' not in message.path:        #if the message still has a valid path
            next = int(message.path[len(message.path) - 1])  # get next node in path
            s = int(message.bands[len(message.bands) - 1])

            # if next == message.src:                                     #if the next node is src then pop it off
            #     next = int(message.path.pop())

            # print("Time: ", t, " try sending msg ", str(message.ID), " from " + str(message.curr), " to ", next,
            #       " over band: ", s - 1)
            # print("genT: ", message.T, " src: ", message.src, " des: ", message.des, " path: ", message.path)

            #Change s in between 0 and S
            s = s % 10
            # print("S is greater 9, ", s)

            # If two nodes are not in communication range
            # if message.curr != next and self.is_in_communication_range(message.curr, next, t, s - 1) == False:
            #     #we keep it to the current node
            #     print("========= Not in range. Do not forward the message." + str(message.curr) + " " + str(next))
            #
            # else:
            if self.is_in_communication_range(message.curr, next, t, s - 1) == True:
                message.path.pop()
                message.bands.pop()

                # calculate total energy consumption from ADJ_E matrix
                if message.totalDelay < math.inf:
                    message.totalEnergy += ADJ_E[message.curr, next, int(message.totalDelay), 0]
                    # calculate total delay from ADJ_T matrix
                    message.totalDelay += ADJ_T[message.curr, next, int(message.totalDelay), 0]

                # if message.curr != next:  # temporal link
                #     print("Store the message for this time epoch")
                # else:

                if message.curr != next:
                    # print("Remove the node: ", next)
                    #handle message transferred
                    nodes[next].buf.append(message)							    #add message to next node buffer
                    nodes[message.curr].buf.remove(message)						#remove message from current node buffer
                    message.curr = next								            #update messages current node
                    self.buf_size -= 1                                          #update current nodes buffer


        else: #Message has been delivered
            nodes[message.curr].buf.remove(message)  # remove message from destination node buffer

            # if message has reached its destination
            # if len(message.path) == 0: #and message.src != message.des: # and message.T  + message.totalDelay <= T:
            if t <= T: #delivered time is less than the allowed TTL deadline
                output_file = open(path_to_folder + delivery_file_name, "a")        #print confirmation to output file

                output_msg = str(message.ID) + "\t" + str(message.src) + "\t" + str(message.des) + "\t" + str(
                    message.T) + "\t" + str(int(t)) + "\t" + str(message.size) +"\t" + str(
                    int(message.totalDelay)) + "\t" + str(message.totalEnergy) + "\n"

                output_file.write(output_msg)
                output_file.close()

# TODO: This "0" in the matrices ADJ_E and ADJ_T should be replaced by message type
# TODO: message type must come from message class (for now, its hardcoded)


#TODO: Here before transferring message to the next node, we need to check if the next node is in communication range
#TODO: with current node over the spectrum band
#TODO: Like we obtained LLC path by reading the path file, we need to get the spectrum band as well in similar fashion
#TODO: Currently, we have both path and spectrum information in LLC_PATH_Spectrum.txt file (need to be kept separately for easy read)

#TODO: To find out if two nodes are in communication range at a certain time epoch, we need to look at those node files.
#TODO: E.g., if we need to find if node 0 and 1 are in communication range at time 3 seconds, then, we open files 0.txt and 1.txt.
#TODO: Then, we get coordinates of nodes 0 and 1 at time 3 seconds, and see if the euclidean distance between them are less than that of
#TODO: communication range of spectrum band
