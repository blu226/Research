import numpy
import math
from STB_help import *
from path import *
from constants import *

#Initialization

specBW = numpy.zeros(shape =(V, V, S, T))       # Initialize the dynamic spectrum bandwidth

ADJ = numpy.empty(shape=(V, V, S, T, T))      # Initialize the Adjacency matrix - Just either links exists or not
ADJ.fill(math.inf)

ADJ_E = numpy.empty(shape=(V, V, S, T, len(M)))      # Initialize the Adjacency matrix - Energy part
ADJ_E.fill(math.inf)

LINK_EXISTS = numpy.empty(shape=(V, V, S, T, T))
LINK_EXISTS.fill(math.inf)

# MODULES

tau = computeTau()                              # Get the discrete time interval period
specBW = getSpecBW(specBW, V, S, T)             # Get the dynamic spectrum bandwidth

# ADJ = initializeADJ(ADJ, V, S, T, tau, specBW)
# printADJ(ADJ, V, S, T, tau)
LINK_EXISTS = createLinkExistenceADJ(LINK_EXISTS)
# printADJ(LINK_EXISTS, V, S, T, tau)

#Initialize the ADJ_T for LLC path
ADJ_T, Parent = computeADJ_T_2(specBW, LINK_EXISTS, V, S, T, M, tau)
LLC_Path, Parent, Spectrum = LLC_PATH_ADJ_2(ADJ_T, Parent, V, S, T, M, tau)


# print4d(LLC_Path, Parent, Spectrum)
# print5d(ADJ_T)

# PRINT_PATH_2(LLC_Path, Parent, Spectrum)

#
# print("Spectrum")
# print4d(Spectrum)