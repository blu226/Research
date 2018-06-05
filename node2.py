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

    def get_attributes(self, curr, ts, te, s):
        with open(validate_data_directory + str(curr) + ".txt", "r") as fc:
            lines = fc.readlines()[1:]

        curr_coorX = [-1 for i in range(te-ts)]
        curr_coorY  = [-1 for i in range(te-ts)]


        k = 0
        for i in range(len(lines)):
            curr_line_arr = lines[i].strip().split()

            if int(float(curr_line_arr[0])) >= ts and int(float(curr_line_arr[0])) < te:
                curr_coorX[k] = curr_line_arr[1]
                curr_coorY[k] = curr_line_arr[2]
                k = k + 1
        return curr_coorX, curr_coorY

    def is_in_communication_range(self, curr, next, ts, te, s):
        curr_coorX, curr_coorY = self.get_attributes(curr, ts + StartTime, te + StartTime,  s)
        next_coorX, next_coorY = self.get_attributes(next, ts + StartTime, te + StartTime, s)

        # print(curr_coorX)
        # print("Dist: ", euclideanDistance(curr_coorX, curr_coorY, next_coorX, next_coorY), s, spectRange[s])

        for i in range(len(curr_coorX)):
            if curr_coorX[i] == -1 or next_coorX[i] == -1:
                return False

            else:
                dist = euclideanDistance(curr_coorX[i], curr_coorY[i], next_coorX[i], next_coorY[i])
                if dist > spectRange[s]:
                    #print("t: " + str(t) + " X: " + str(curr_coorX) + " Y: " + str(curr_coorY))
                    return False

        return True

    def compute_transfer_time(self, size, s, specBW, i, j, t, msg):
        numerator = math.ceil(size / specBW[i, j, s, t]) * (t_sd + idle_channel_prob * t_td)
        time_to_transfer = tau * math.ceil(numerator / tau)
        # print ( msg.ID, i, " - ", msg.des, msg.T, " Int: ", j, t, time_to_transfer)
        return time_to_transfer

    def send_message(self, net, message, t, specBW):

        nodes = net.nodes

        #print("\n Message ID: " + str(message.ID) + " path: " + str(message.path))         #console output for debugging

        if len(message.path) > 0 and '' not in message.path:        #if the message still has a valid path
            next = int(message.path[len(message.path) - 1])  # get next node in path
            s = int(message.bands[len(message.bands) - 1])

            #Change s in between 0 and S
            s = s % 10

            if message.curr == next:
                message.path.pop()
                message.bands.pop()

            elif message.curr != next and message.last_sent <= t:
                transfer_time = self.compute_transfer_time(message.size, s - 1, specBW, message.curr, next, t, message)

                if self.is_in_communication_range(message.curr, next, t, t + transfer_time, s - 1) == True:
                    # print("In range: ", message.curr, next, t, t + transfer_time)
                    message.path.pop()
                    message.bands.pop()
                    message.last_sent = t + transfer_time

                    if message.curr != next:
                        # print("Remove the node: ", next)
                        #handle message transferred
                        nodes[next].buf.append(message)							    #add message to next node buffer
                        nodes[message.curr].buf.remove(message)						#remove message from current node buffer
                        message.curr = next								            #update messages current node
                        self.buf_size -= 1                                          #update current nodes buffer


        #This is else to the len(message.path) > 0
        else: #Message has been delivered
            nodes[message.curr].buf.remove(message)  # remove message from destination node buffer

            if t <= T: #delivered time is less than the allowed TTL deadline
                output_file = open(path_to_folder + delivery_file_name, "a")        #print confirmation to output file

                if t > message.last_sent:
                    message.last_sent = t

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
