import numpy
import math
from STB_help import *
from constants import *

#Initialization

V = NoOfDMs                 # Number of nodes in the STB graph is equivalent to number of data mules we have in the DSA overlay network

specBW = numpy.zeros(shape =(V, V, S, T))       # Initialize the dynamic spectrum bandwidth

ADJ = numpy.empty(shape=(V, V, S, T, T))      # Initialize the Adjacency matrix - Just either links exists or not
ADJ.fill(math.inf)

ADJ_E = numpy.empty(shape=(V, V, S, T, T))      # Initialize the Adjacency matrix - Energy part
ADJ_E.fill(math.inf)

ADJ_MSG    = numpy.empty(shape = (V, V, S, T, len(M))) # Adjacency matrix that holds message transmission delay for each message for each node pair
ADJ_MSG.fill(math.inf)

LINK_EXISTS = numpy.empty(shape=(4, 4, 2, 5, 5))
LINK_EXISTS.fill(math.inf)

# MODULES

tau = computeTau()                              # Get the discrete time interval period
specBW = getSpecBW(specBW, V, S, T)             # Get the dynamic spectrum bandwidth

# ADJ = initializeADJ(ADJ, V, S, T, tau, specBW)
# printADJ(ADJ, V, S, T, tau)
LINK_EXISTS = createLinkExistenceADJ(LINK_EXISTS)
# printADJ(LINK_EXISTS, V, S, T, tau)

ADJ_MSG = computeADJ_MSG(specBW, ADJ_MSG, LINK_EXISTS, V, S, T, M, tau)
ADJ_MSG, ADJ_E = computeADJ_E(specBW, ADJ_MSG, ADJ_E, LINK_EXISTS, V, S, T, M, tau)
# printADJ_MSG(ADJ_MSG, V, S, T, M, tau)

# ADJ_E = initializeADJ2(ADJ_E, V, S, T, tau, specBW, specBW)      #Initialize the 5D adjacency matrix
# print("ADJ_E MATRIX")
# printADJ(ADJ_E, V, S, T, tau)
#
LLC_Path, Parent, Spectrum = LLC_PATH_ADJ(ADJ_MSG, V, S, T, M, tau)
#
print("Least Latency Cost Path")
printADJ_4D(LLC_Path, V, T, M)

# print("Parent")
# print4d(Parent)
#
# print("Spectrum")
# print4d(Spectrum)

