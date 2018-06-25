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
        self.band_usage = [0, 0, 0, 0]

        self.parent = -1


    def set(self, lastSent,  parent):
        self.last_sent = lastSent
        self.parent = parent


    def band_used(self, s):
        self.band_usage[s] += 1


