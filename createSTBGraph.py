import random
import numpy
import math

from constants import *

def computeTau():
    return 1

def getMinBWFromDMFiles(i, j, s, t):
    with open("Data/"+ str(i) + ".txt") as fi:
        next(fi)
        iLines = fi.readlines()
    fi.close()

    with open("Data/"+ str(j) + ".txt") as fj:
        next(fj)
        jLines = fj.readlines()
    fj.close()

    currBW = -1
    for iLine in iLines:
        iLineArr = iLine.strip().split(' ')
        for jLine in jLines:
            jLineArr = jLine.strip().split(' ')
            # print ("At time " + str(t) + " Values: " + iLineArr[0] + " " + jLineArr[0])
            if int(iLineArr[0]) == t and int(jLineArr[0]) == t:
                # print("At time " + str(t) + " Values: " + iLineArr[3] + " " + jLineArr[3])
                if int(iLineArr[s+3]) < int(jLineArr[s+3]):
                    currBW = int(iLineArr[s+3])
                    return currBW
                else:
                    currBW = int(jLineArr[s+3])
                    return currBW
            # else:
            #     print (str(t) + " " + iLineArr[0] + " " + jLineArr[0])
    return currBW

def getSpecBW(specBW, V, S, T):
    for i in range(V):
        for j in range(V):
            for s in range(S):
                for t in range(T):
                    if i == j:
                        specBW[i, j, s, t] = 0
                    else:
                        specBW[i, j, s, t] = getMinBWFromDMFiles(i, j, s, t)
                        print ("i= " + str(i) + " j= " + str(j) + " s= " + str(s) + " t= " + str(t) + " BW= " + str(specBW[i, j, s, t]))
    return specBW

def linkExists(i, j, s, ts , te):
    with open("Data/" + str(i) + ".txt") as fi:
        next(fi)
        iLines = fi.readlines()
    fi.close()

    with open("Data/" + str(j) + ".txt") as fj:
        next(fj)
        jLines = fj.readlines()
    fj.close()

    return True

def initializeADJ(V, S, T, tau):
    ADJ = numpy.zeros(shape=(V, V, S, T, T))
    for i in range(V):
        for j in range(V):
            for s in range(S):
                for ts in range(0, T, tau):
                    for te in range(ts, T, tau):
                        if linkExists(i, j, s, ts, te) == True:
                            ADJ[i,j,s,ts,te] = 1            # spatial link
                            if te == ts + 1:
                                ADJ[i,i,s,ts,te] = 1        # temporal link



specBW = numpy.zeros(shape =(NoOfDMs, NoOfDMs, S, T))
tau = computeTau()
specBW = getSpecBW(specBW, NoOfDMs, S, T)

initializeADJ(NoOfDMs, S, T, tau)






