from constants import *

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


    def send_message(self, net, message, t, ADJ_T, ADJ_E):
        nodes = net.nodes

        print("Message ID: " + str(message.ID) + " path: " + str(message.path))         #console output for debugging

        if len(message.path) > 0 and '' not in message.path:                                   #if the message still has a valid path
            next = int(message.path.pop())							#get next node in path

            if next == message.src:                                     #if the next node is src then pop it off
                next = int(message.path.pop())

            # TODO: This "0" in the matrices ADJ_E and ADJ_T should be replaced by message type
            # TODO: message type must come from message class (for now, its always 0)
            # calculate total energy consumption from ADJ_E matrix
            message.totalEnergy += ADJ_E[message.curr, next, int(message.totalDelay), 0]
            # calculate total delay from ADJ_T matrix
            message.totalDelay += ADJ_T[message.curr, next, int(message.totalDelay), 0]

            # print(str(ADJ_E[message.curr, next, int(message.totalDelay), 0]) + " " + str(message.curr) + " " + str(next) + " " + str(message.totalDelay))

            #TODO: Here before transferring message to the next node, we need to check if the next node is in communication range
            #TODO: with current node over the spectrum band
            #TODO: Like we obtained LLC path by reading the path file, we need to get the spectrum band as well in similar fashion
            #TODO: Currently, we have both path and spectrum information in LLC_PATH_Spectrum.txt file (need to be kept separately for easy read)

            #TODO: To find out if two nodes are in communication range at a certain time epoch, we need to look at those node files.
            #TODO: E.g., if we need to find if node 0 and 1 are in communication range at time 3 seconds, then, we open files 0.txt and 1.txt.
            #TODO: Then, we get coordinates of nodes 0 and 1 at time 3 seconds, and see if the euclidean distance between them are less than that of
            #TODO: communication range of spectrum band

            nodes[next].buf.append(message)							    #add message to next node buffer
            nodes[message.curr].buf.remove(message)						#remove message from current node buffer
            print("Message ", str(message.ID), " sent from " + str(message.curr), " to ", next) #console output for debugging
            message.curr = next								            #update messages current node
            self.buf_size -= 1                                          #update current nodes buffer

        if message.curr == message.des and len(message.path)  == 0:      #if message has reached its destination
            output_file = open(path_to_folder + "LLC_delivery_confirmation.txt", "a")        #print confirmation to output file
            output_msg = str(message.ID) + "\t" + str(message.src) + "\t" + str(message.des) + "\t\t" + str(message.T) + "\t\t" + str(message.T + int(message.totalDelay))+ "\t\t" + str(int(message.totalDelay)) + "\t\t\t" + str(message.totalEnergy) + "\n"
            output_file.write(output_msg)
            output_file.close()

            nodes[message.curr].buf.remove(message)                     #remove message from destination node buffer
