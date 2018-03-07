import numpy
import math
from STB_help import *
from constants import *

#Initialization

V = NoOfDMs                 # Number of nodes in the STB graph is equivalent to number of data mules we have in the DSA overlay network

specBW = numpy.zeros(shape =(V, V, S, T))       # Initialize the dynamic spectrum bandwidth

ADJ = numpy.empty(shape=(V, V, S, T, T))      # Initialize the Adjacency matrix - Just either links exists or not
ADJ.fill(math.inf)

ADJ_E = numpy.empty(shape=(V, V, S, T, len(M)))      # Initialize the Adjacency matrix - Energy part
ADJ_E.fill(math.inf)

ADJ_MSG    = numpy.empty(shape = (V, V, S, T, len(M))) # Adjacency matrix that holds message transmission delay for each message for each node pair
ADJ_MSG.fill(math.inf)

LINK_EXISTS = numpy.empty(shape=(4, 4, 2, 5, 5))
LINK_EXISTS.fill(math.inf)

# LLC = Least Latency Cost Path
LLC_PATH = numpy.empty(shape=(V, V, T, len(M)))
LLC_PATH.fill(math.inf)

Parent = numpy.empty(shape=(V, V, T, len(M)))
Parent.fill(-1)

Spectrum = numpy.empty(shape=(V, V, T, len(M)))
Spectrum.fill(-1)

# MODULES

tau = computeTau()                              # Get the discrete time interval period
specBW = getSpecBW(specBW, V, S, T)                     # Get the dynamic spectrum bandwidth

# ADJ = initializeADJ(ADJ, V, S, T, tau, specBW)
# printADJ(ADJ, V, S, T, tau)
LINK_EXISTS = createLinkExistenceADJ(LINK_EXISTS)
# printADJ(LINK_EXISTS, V, S, T, tau)

# ADJ_MSG = computeADJ_MSG(specBW, ADJ_MSG, LINK_EXISTS, V, S, T, M, tau)
ADJ_MSG, ADJ_E = computeADJ_E(specBW, ADJ_MSG, ADJ_E, LINK_EXISTS, V, S, T, M, tau)
ADJ_MSG, ADJ_TE = computeADJ_TE(specBW, ADJ_MSG, ADJ_E, LINK_EXISTS, V, S, T, TTL, M, tau)

LLC_Path, Parent, Spectrum = LLC_PATH_ADJ(ADJ_MSG, LLC_PATH, Parent, Spectrum, V, S, T, M, tau)
LEC_Path, Parent_E, Spectrum_E = LEC_PATH_ADJ(ADJ_MSG, ADJ_E, V, S, T, TTL, M, tau)
TLEC_Path, Parent_TE, Spectrum_TE = TLEC_PATH_ADJ(ADJ_MSG, ADJ_TE, V, S, T, TTL, M, tau)

# printADJ_4D(LLC_Path, V, T, M)
print("\nLLC and LEC paths are as follows: \n")
print("i j t m  =  LLC   LEC")
printADJ_MSG_E_4D(LLC_Path, LEC_Path, TLEC_Path, V, T, M)
#
# print("\nLLC LEC Parent")
# print("i j t m  =  P_LLC   P_LEC")
# printADJ_MSG_E_4D(Parent, Parent_E, Parent_TE, V, T, M)

#
# print("Spectrum")
# print4d(Spectrum)

