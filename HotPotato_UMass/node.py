#NODE CLASS
from constants import *
from message import *
import math




def can_transfer(size, s, seconds, specBW, i, j, t, msg):
    numerator = math.ceil(size / specBW[i, j, s, t]) * (t_sd + idle_channel_prob * t_td)
    time_to_transfer = tau * math.ceil(numerator / tau)
    # if msg.ID == 1:
    #     print("Message : ", msg.ID, msg.src, msg.des, " Int: ", i, j)

    if time_to_transfer <= seconds:
        return True
    else:
        return False

def find_delay(size, s, specBW, i, j, t):
    bw = specBW[i,j,s,t]
    return size/bw


#Function init: initialize variables
class node(object):
    def __init__(self, id):
        self.ID = int(id)
        self.buf = []

    def choose_messages_to_send(self, mesID):
        all_mes_list = []
        mes_to_send = []

        for mes in self.buf:
            if mes.ID == mesID:
                all_mes_list.append(mes)

        num_mess_to_send = int(math.floor(len(all_mes_list)/2))

        for i in range(num_mess_to_send):
            mes_to_send.append(all_mes_list[i])

        return mes_to_send


#Function send_message: sends message to a node if it doesn't have the message already
    def try_sending_message(self, des_node, mes, ts, LINK_EXISTS, specBW):

        if mes.last_sent <= ts:
            max_end = ts + maxTau

            if max_end > T:
                return False

            for te in range(ts+1, max_end):
                spec_to_use = []

                for s in range(4):

                    if LINK_EXISTS[self.ID, des_node.ID, s, int(ts - startTime), int(te - startTime)] == 1:
                        spec_to_use.append(s)

                for spec in range(len(spec_to_use)):
                    if can_transfer(mes.size, spec_to_use[spec], (te - ts), specBW, self.ID, des_node.ID, ts, mes):

                       #append messages to des buffer and remove from src buffer
                       self.buf.remove(mes)

                       mes.set(te, self.ID)
                       des_node.buf.append(mes)

                       return True

            return False




