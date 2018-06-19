#NODE CLASS
from constants import *
from message import *
import random
import math
import numpy



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
        self.energy = 0
        self.buf = []

#Function send_message: sends message to a node if it doesn't have the message already
    def try_sending_message(self, des_node, mes, ts, replicaID, LINK_EXISTS, specBW):

        if mes.last_sent <= ts:
            max_end = ts + maxTau

            if max_end > T:
                max_end = T

            for te in range(ts+1, max_end):
                spec_to_use = []

                for s in S:

                    if LINK_EXISTS[self.ID, des_node.ID, s, int(ts - startTime), int(te - startTime)] == 1:
                        spec_to_use.append(s)

                for spec in range(len(spec_to_use)):
                    if can_transfer(mes.size, spec_to_use[spec], (te - ts), specBW, self.ID, des_node.ID, ts, mes):
                        #calculate energy consumed
                        sensing_energy = math.ceil(mes.size / (specBW[self.ID, des_node.ID, spec_to_use[spec], ts])) * t_sd * sensing_power
                        switching_energy = math.ceil(mes.size / (specBW[self.ID, des_node.ID, spec_to_use[spec], ts])) * idle_channel_prob * switching_delay
                        transmission_energy = math.ceil(mes.size / specBW[self.ID, des_node.ID, spec_to_use[spec], ts]) * idle_channel_prob * t_td * spectPower[spec_to_use[spec]]

                        consumedEnergy = sensing_energy + switching_energy + transmission_energy
                        consumedEnergy = round(consumedEnergy, 2)

                        self.energy += consumedEnergy
                        des_node.energy += consumedEnergy


                        new_message = message(mes.ID, mes.src, mes.des, mes.genT, mes.size, [mes.band_usage[0], mes.band_usage[1], mes.band_usage[2], mes.band_usage[3]])
                        new_message.set(te, replicaID, te, self.ID)
                        new_message.band_used(spec_to_use[spec])
                        if new_message.ID == debug_message:
                            print("time: ", ts, "src", self.ID, "des", des_node.ID, "prev Bands used", mes.band_usage, "next band ", new_message.band_usage)
                        des_node.buf.append(new_message)


                        return True
            return False

    def send_message2(self, des_node, mes, ts, replicaID, LINK_EXISTS, specBW):

        if mes.last_sent < ts:

            S = [0, 2, 1, 3]

            for s in S:

                i = self.ID
                j = des_node.ID

                delay = find_delay(mes.size, s, specBW, i, j, ts)
                te = ts + delay

                if te < T:

                    if LINK_EXISTS[i, j, s, ts, te] == 1:
                        new_message = message(mes.ID, mes.src, mes.des, mes.genT, mes.size, mes.band_usage)
                        new_message.set(te, replicaID, te, i)
                        des_node.buf.append(new_message)

                        return True


        return False




