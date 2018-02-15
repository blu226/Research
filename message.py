class Message(object):                                                                          #Message Object
    def __init__(self, src, des, name, ttl, path, size):
        self.src = src                                                                  #message source node
        self.des = des                                                                  #message destination node
        self.ttl = ttl                                                                  #message ttl
        self.name = name                                                                #message name
        self.curr = src                                                                 #current node message is located at
        self.path = path                                                                #path for message to follow
        self.size = size 
