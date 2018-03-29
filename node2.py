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


    def send_message(self, net, message, t, ADJ_T, ADJ_TE):
        nodes = net.nodes

        print("Message ID: " + str(message.ID) + " path: " + str(message.path))         #console output for debugging

        if len(message.path) > 0 and '' not in message.path:                                   #if the message still has a valid path
            next = int(message.path.pop())							#get next node in path

            if next == message.src:                                     #if the next node is src then pop it off
                next = int(message.path.pop())
                # calculate total energy consumption from ADJ_TE matrix
            message.totalEnergy += ADJ_TE[message.curr, next, int(message.totalDelay)]
            message.totalDelay += ADJ_T[message.curr, next, int(message.totalDelay)]  # calculate total delay from ADJ_T matrix
            print(str(ADJ_TE[message.curr, next, int(message.totalDelay)]) + " " + str(message.curr) + " " + str(next) + " " + str(message.totalDelay))

            nodes[next].buf.append(message)							    #add message to next node buffer
            nodes[message.curr].buf.remove(message)						#remove message from current node buffer
            print("Message ", str(message.ID), " sent from " + str(message.curr), " to ", next) #console output for debugging
            message.curr = next								            #update messages current node
            self.buf_size -= 1                                          #update current nodes buffer

        if message.curr == message.des and len(message.path)  ==0:      #if message has reached its destination

            output_file = open("Delivery_Confirmation.txt", "a")        #print confirmation to output file
            output_msg = str(message.ID) + "\t" + str(message.src) + "\t" + str(message.des) + "\t\t" + str(message.T) + "\t\t" + str(message.T + int(message.totalDelay))+ "\t\t" + str(int(message.totalDelay)) + "\t\t\t" + str(message.totalEnergy) + "\n"
            output_file.write(output_msg)
            output_file.close()

            nodes[message.curr].buf.remove(message)                     #remove message from destination node buffer
