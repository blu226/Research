#MESSAGE CLASS

#Function init: initialize variables
class message(object):
    def __init__(self, ID, src, des, genT, size):
        self.src = int(src)
        self.des = int(des)
        self.ID = int(ID)
        self.size = int(size)
        self.genT = int(genT)
        self.last_sent = int(genT)
        self.parent = -1


    def set(self, lastSent, parent):
        self.last_sent = lastSent
        self.parent = parent


