from STB_help import *
from path import *
from TLEC_path import *
from constants import *
import pickle


directory = "Lexington/Day1"
sample_directory = "Data/"
# tau = computeTau()                              # Get the discrete time interval period

print("Spectrum bandwidth assigned: ")
specBW = getSpecBW(directory, V, S, T)             # Get the dynamic spectrum bandwidth

print("Load LINK Exists: ")
# LINK_EXISTS = createLinkExistenceADJ()
LINK_EXISTS = pickle.load(open("LINK_EXISTS.txt", "rb"))

print("Initialization started: ")
ADJ_T, Parent, Spectrum, ADJ_E = computeADJ_T_2(specBW, LINK_EXISTS)

print("LLC path computation started: ")
LLC_Path, Parent, Spectrum, ELC_Path = LLC_PATH_ADJ_2(ADJ_T, ADJ_E, Parent, Spectrum, V, T, M)

# ADJ_T_file = open("ADJ_T.txt", 'wb')
# pickle.dump(ADJ_T, ADJ_T_file)
# ADJ_T_file.close()

print("LLC paths are: ")
PRINT_LLC_PATH_FILE(LLC_Path,  ELC_Path, Parent, Spectrum)

# ADJ_TE, Parent_TE, Spectrum_TE, ADJ_TL = computeADJ_T_TE(specBW, LINK_EXISTS, tau)
# TLEC_Path, Parent_TE, Spectrum_TE, TLLC_Path = TLEC_PATH_ADJ_2(ADJ_TL, ADJ_TE, Parent_TE, Spectrum_TE)

# ADJ_TE_file = open("ADJ_TE.txt", 'wb')
# pickle.dump(ADJ_TE, ADJ_TE_file)
# ADJ_TE_file.close()

# TLEC_file = open("TLEC_path.txt", 'wb')
# pickle.dump(TLEC_Path, TLEC_file)
# TLEC_file.close()

# PRINT_TLEC_PATH_FILE(TLEC_Path, Parent_TE, Spectrum_TE, TLLC_Path)
