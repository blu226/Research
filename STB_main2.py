import numpy
import math
from STB_help import *
from constants import *

#Initialization

specBW = numpy.zeros(shape =(V, V, S, T))       # Initialize the dynamic spectrum bandwidth

ADJ = numpy.empty(shape=(V, V, S, T, T))      # Initialize the Adjacency matrix - Just either links exists or not
ADJ.fill(math.inf)

ADJ_E = numpy.empty(shape=(V, V, S, T, len(M)))      # Initialize the Adjacency matrix - Energy part
ADJ_E.fill(math.inf)

ADJ_T    = numpy.empty(shape = (V, V, S, T, len(M))) # Adjacency matrix that holds message transmission delay for each message for each node pair
ADJ_T.fill(math.inf)

LINK_EXISTS = numpy.empty(shape=(5, 5, 3, 6, 6))
LINK_EXISTS.fill(math.inf)

# MODULES

tau = computeTau()                              # Get the discrete time interval period
specBW = getSpecBW(specBW, V, S, T)                     # Get the dynamic spectrum bandwidth

# ADJ = initializeADJ(ADJ, V, S, T, tau, specBW)
# printADJ(ADJ, V, S, T, tau)
LINK_EXISTS = createLinkExistenceADJ(LINK_EXISTS)
# printADJ(LINK_EXISTS, V, S, T, tau)

#Initialize the ADJ_T for LLC path
ADJ_T = computeADJ_T(specBW, ADJ_T, LINK_EXISTS, V, S, T, M, tau)
LLC_Path, Parent, Spectrum = LLC_PATH_ADJ(ADJ_T, V, S, T, M, tau)

ADJ_T, ADJ_E = computeADJ_E(specBW, ADJ_T, ADJ_E, LINK_EXISTS, V, S, T, M, tau)
LEC_Path, Parent_E, Spectrum_E = LEC_PATH_ADJ(ADJ_T, ADJ_E, V, S, T, M, tau)

ADJ_T, ADJ_TE = computeADJ_TE(specBW, ADJ_T, ADJ_E, LINK_EXISTS, V, S, T, TTL, M, tau)
TLEC_Path, Parent_TE, Spectrum_TE = TLEC_PATH_ADJ(ADJ_T, ADJ_TE, V, S, T, TTL, M, tau)

# printADJ_4D(LLC_Path, V, T, M)
#print("\nLLC and LEC paths are as follows: \n")
#print("i j t m  =  LLC   LEC   TLEC")
#printADJ_T_E_4D(LLC_Path, LEC_Path, TLEC_Path, V, T, M, tau)
#
print("\nLLC LEC Parent")
print("i j t m  =  P_LLC   P_LEC")
#printADJ_T_E_4D(Parent, Parent_E, Parent_TE, V, T, M, tau)
PRINT_PATH(Parent_E)

#
# print("Spectrum")
# print4d(Spectrum)