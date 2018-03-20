from STB_help import *
from path import *
from TLEC_path import *
from constants import *

#Initialization

specBW = numpy.zeros(shape =(V, V, S, T))       # Initialize the dynamic spectrum bandwidth

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

ADJ_T, Parent, Spectrum = computeADJ_T_2(specBW, LINK_EXISTS, tau)
LLC_Path, Parent, Spectrum = LLC_PATH_ADJ_2(ADJ_T, Parent, Spectrum, V, S, T, M, tau)


ADJ_TE, Parent_TE, Spectrum_TE = computeADJ_TE_2(specBW, LINK_EXISTS, tau)
TLEC_Path, Parent_TE, Spectrum_TE = TLEC_PATH_ADJ_2(ADJ_T, ADJ_TE, Parent_TE, Spectrum_TE)


print("i j ts m")
# print4d(LLC_Path, TLEC_Path)
# print4d1(TLEC_Path)
#print("i j s t m")
# print5d(ADJ_TE)

PRINT_PATH_2(LLC_Path, Parent, Spectrum)

#
# print("Spectrum")
# print4d(Spectrum)