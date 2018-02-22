import numpy
import math
from STB_help import *

V = NoOfDMs                 # Number of nodes in the STB graph is equivalent to number of data mules we have in the DSA overlay network
tau = computeTau()                              # Get the discrete time interval period

#Initialization
specBW = numpy.zeros(shape =(V, V, S, T))       # Initialize the dynamic spectrum bandwidth
ADJ_E = numpy.empty(shape=(V, V, S, T, T))      # Initialize the Adjacency matrix
ADJ_E.fill(math.inf)

specBW = getSpecBW(specBW, V, S, T)                     # Get the dynamic spectrum bandwidth
ADJ_E = initializeADJ(ADJ_E, V, S, T, tau, specBW)      #Initialize the 5D adjacency matrix
print("ADJ_E MATRIX")
printADJ(ADJ_E, V, S, T, tau)

LEC_Path, Parent, Spectrum = LEC_PATH_ADJ(ADJ_E, V, S, T, tau)

print("Shortest Path")
print4d(LEC_Path)

print("Parent")
print4d(Parent)

print("Spectrum")
print4d(Spectrum)

