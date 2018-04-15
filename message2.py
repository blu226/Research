class Message(object):                                                                          #Message Object
    def __init__(self, src, des, T, ID, ttl, size, path, bands, delay, energy):
        self.src = int(src)                                                                  #message source node
        self.des = int(des)                                                                  #message destination node
        self.T = int(T)                                                                      #time created
        self.ttl = int(ttl)                                                                  #message ttl
        self.ID = int(ID)                                                                #message name
        self.curr = int(src)                                                                 #current node message is located at
        self.path = path                                                                #path for message to follow
        self.bands = bands
        self.size = int(size)
        self.totalDelay = 0
        self.totalEnergy = 0

