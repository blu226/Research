import pickle
import math
from computeHarvesine import *
from constants import *
from STB_help import *

class Node(object):                                                                     #Node Object
    def __init__(self, name):
        self.ID = name                                                                #Node ID or name (string)
        self.buf = []                                                                   #Node message buffer
        self.coord = []
        self.energy = 0
        self.buf_size = 0

    def load_pkl(self):
        self.coord = pickle.load(open(pkl_folder + self.ID + ".pkl", "rb"))

    def print_buf(self):
        # print(str(self.name) +  " Buffer ")
        if len(self.buf) == 0:
            print(">>>>>>>>>>>>> No messages")

        for i in range(len(self.buf)):
            message = self.buf[i].ID
            print("Message ID: " + str(message))

    def get_attributes(self, ts, te):
        curr_coorX = []
        curr_coorY  = []

        if te > T:
            te = T

        for i in range(ts, te):
            curr_coorX.append(self.coord[i][0])
            curr_coorY.append(self.coord[i][1])

        return curr_coorX, curr_coorY



    def is_in_communication_range(self, curr, next, ts, te, s, msg):

        if te > T:
            return False

        curr_coorX, curr_coorY = curr.get_attributes(ts, te)
        next_coorX, next_coorY = next.get_attributes(ts, te)

       # print(curr_coorX, curr_coorY, next_coorX, next_coorY, s)
        # print("Dist: ", euclideanDistance(curr_coorX, curr_coorY, next_coorX, next_coorY), s, spectRange[s])

        for i in range(len(curr_coorX)):
            if curr_coorX[i] == -1 or next_coorX[i] == -1 or curr_coorX[i] == '0' or next_coorX[i] == '0' or curr_coorX[i] == ' ' or next_coorX[i] == ' ':
                return False

            else:
                dist = funHaversine(float(curr_coorY[i]),float(curr_coorX[i]), float(next_coorY[i]), float(next_coorX[i]))
                if int(debug_message) == int(msg.ID):
                    print("dist =", dist, "specRange =", spectRange[s])
                if dist > spectRange[s]:
                    #print("t: " + str(t) + " X: " + str(curr_coorX) + " Y: " + str(curr_coorY))
                    return False

        return True

    def compute_transfer_time(self, msg, s, specBW, i, j, t):
        numerator = math.ceil(msg.size / specBW[i, j, s, t]) * (t_sd + idle_channel_prob * t_td)
        time_to_transfer = tau * math.ceil(numerator / tau)
        return time_to_transfer

    def send_message(self, net, message, ts, specBW, LINK_EXISTS):

        nodes = net.nodes

        if len(message.path) > 0 and '' not in message.path:        #if the message still has a valid path
            next = int(message.path[len(message.path) - 1])  # get next node in path
            s = int(message.bands[len(message.bands) - 1])

            # Change s in between 0 and S
            if s > 9:
                s = s % 10
            s = s - 1



            # self.is_in_communication_range(message.curr, next, t, s - 1)
            if message.curr != next and message.last_sent <= ts:

                transfer_time = self.compute_transfer_time(message, s, specBW, message.curr, next, ts)
                te = ts + transfer_time

                if te >= T:
                    te = T - 1
                # print("curr: ", message.curr, "next: ", next)
                # if self.is_in_communication_range(nodes[message.curr], nodes[next], ts, te, s, message) == True:
                if LINK_EXISTS[int(nodes[message.curr].ID), int(nodes[next].ID), s, ts, te] == 1:
                    # calculate energy consumed
                    sensing_energy = math.ceil(message.size / (specBW[message.curr, next, s, ts])) * t_sd * sensing_power
                    switching_energy = math.ceil(message.size / (specBW[message.curr, next, s, ts])) * idle_channel_prob * switching_delay
                    transmission_energy = math.ceil(message.size / specBW[message.curr, next, s, ts]) * idle_channel_prob * t_td * spectPower[s]

                    consumedEnergy = sensing_energy + switching_energy + transmission_energy
                    consumedEnergy = round(consumedEnergy, 2)

                    self.energy += consumedEnergy
                    net.nodes[next].energy += consumedEnergy
                    message.path.pop()
                    message.bands.pop()
                    message.last_sent = ts + transfer_time


                    if message.curr != next:
                        # print("Remove the node: ", next)
                        #handle message transferred
                        nodes[next].buf.append(message)							    #add message to next node buffer
                        nodes[message.curr].buf.remove(message)						#remove message from current node buffer
                        message.curr = next								            #update messages current node
                        self.buf_size -= 1                                          #update current nodes buffer

            elif message.curr == next and message.last_sent <= ts:
                message.path.pop()
                message.bands.pop()
                message.last_sent += 1

        #This is else to the len(message.path) > 0
        else: #Message has been delivered
            nodes[message.curr].buf.remove(message)  # remove message from destination node buffer

            # if message has reached its destination
            # if len(message.path) == 0: #and message.src != message.des: # and message.T  + message.totalDelay <= T:
            if ts <= T: #delivered time is less than the allowed TTL deadline
                output_file = open(path_to_folder + delivery_file_name, "a")        #print confirmation to output file

                output_msg = str(message.ID) + "\t" + str(message.src) + "\t" + str(message.des) + "\t" + str(
                    message.T) + "\t" + str(int(message.last_sent)) + "\t" + str(message.size) +"\t" + str(
                    int(message.last_sent - message.T )) + "\t" + str(message.totalEnergy) + "\n"

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
