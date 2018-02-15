class Node(object):                                                                     #Node Object
    def __init__(self, name):
        self.name = name                                                                #Node ID or name (string)
        self.buf = []                                                                   #Node message buffer
        self.netID = 0                                                                  #ID of node in network class (int)
        self.coord = [0, 0]

    def place(self, x, y):                                                              #place node on x-y plane
        self.coord[0] = x
        self.coord[1] = y

    def send_message(self, message, net):                                               #send message
        nodes = net.nodes
        path = message.path                                                             #find path for message to follow
        for i in range(len(path)):                                                      #for each node in the path
            cur = path[i][0]
            next = path[i][1]
            spec = path[i][2]
            print("Hop: ", i)                                                           #print hop number (for debugging purposes)
            time.sleep(1)                                                               #wait 1 sec so messages dont move faster then ep$
            if(i == 0):                                                                 #if message is at sender
                nodes[next].buf.append(message)                                         #copy message to next node's buf
                message.curr = nodes[next].name                                         #update messages's current node status
            elif(i < len(path) - 1):                                                    #if message is not at sender
                nodes[next].buf.append(message)                                         #copy message to next node's buf
                message.curr = nodes[next].name                                         #update message's current node status
                nodes[cur].buf.remove(message)                                          #remove message from previous node's buf
            if i != len(path) - 1:                                                      #if message isn't at destination
                message.ttl -= (message.size / net.adj[cur][next][spec])                #subtract time taken from ttl (msg size / bandwi$
            else:                                                                       #if message is at destination
                if i == 0:                                                              #and there was only 1 hop
                    nodes[next].buf.remove(message)                                     #remove message from destination buffer
                else:                                                                   #if message is at destination and took > 1 hop
                    nodes[cur].buf.remove(message)                                      #remove message from destination buffer
        print("message sent")                                                           #print message sent (for debugging purposes)

    def send(self, message, net):
        t1 = threading.Thread(target = self.send_message, args = (message, net,))
        t1.start()



