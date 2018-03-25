class Node(object):                                                                     #Node Object
    def __init__(self, name):
        self.name = name                                                                #Node ID or name (string)
        self.buf = []                                                                   #Node message buffer
        self.coord = [0, 0]

    def place(self, x, y):                                                              #place node on x-y plane
        self.coord[0] = x
        self.coord[1] = y

    def print_buf(self):
        for i in range(len(self.buf)):
            message = self.buf[i].ID
            print(message)

    def send_message(self, message, net):
        nodes = net.nodes
        if len(message.path) != 0:
            next = int(message.path.pop())							#next node in path
            nodes[next].buf.append(message)							#add message to next node buffer
#            del nodes[message.curr].buf[0]
            nodes[message.curr].buf.remove(message)						#remove message from current node buffer
            message.curr = next								#update messages current node
