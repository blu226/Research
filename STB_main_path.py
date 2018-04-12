from STB_help import *
from path import *
from TLEC_path import *
from constants import *
import pickle


directory = "Lexington/Day1"
sample_directory = "Data/"

# band_type = ["ALL", "TV", "ISM"]
# path_to_folder = "Bands/" + band_type[1] + "/"
# tau = computeTau()                              # Get the discrete time interval period

print("Spectrum bandwidth assigned: ")
specBW = getSpecBW(directory, V, S, T)             # Get the dynamic spectrum bandwidth

print("Load LINK Exists: ")
# LINK_EXISTS = createLinkExistenceADJ()
LINK_EXISTS = pickle.load(open(path_to_folder +"LINK_EXISTS.pkl", "rb"))

print("Initialization started: ")
ADJ_T, Parent, Spectrum, ADJ_E = computeADJ_T_2(specBW, LINK_EXISTS)

print("LLC path computation started: ")
LLC_Path, Parent, Spectrum, ELC_Path = LLC_PATH_ADJ_2(ADJ_T, ADJ_E, Parent, Spectrum, V, T, M)

ADJ_T_file = open(path_to_folder + "ADJ_T.pkl", 'wb')
pickle.dump(ADJ_T, ADJ_T_file)
ADJ_T_file.close()

ADJ_E_file = open(path_to_folder + "ADJ_E.pkl", 'wb')
pickle.dump(ADJ_E, ADJ_E_file)
ADJ_E_file.close()

LLC_path_file = open(path_to_folder + "LLC.pkl", 'wb')
pickle.dump(LLC_Path, LLC_path_file)
LLC_path_file.close()

ELC_path_file = open(path_to_folder + "ELC.pkl", 'wb')
pickle.dump(ELC_Path, ELC_path_file)
ELC_path_file.close()

save_4D_in_file("LLC.txt", LLC_Path)
save_4D_in_file("ELC.txt", ELC_Path)

print("LLC paths are: ")
PRINT_LLC_PATH_FILE(LLC_Path, ELC_Path, Parent, Spectrum)

print("TLEC path computation started: ")
ADJ_TE, Parent_TE, Spectrum_TE, ADJ_TL = computeADJ_T_TE(specBW, LINK_EXISTS, tau)
TLEC_Path, Parent_TE, Spectrum_TE, TLLC_Path = TLEC_PATH_ADJ_2(ADJ_TL, ADJ_TE, Parent_TE, Spectrum_TE)

ADJ_TE_file = open(path_to_folder + "ADJ_TE.pkl", 'wb')
pickle.dump(ADJ_TE, ADJ_TE_file)
ADJ_TE_file.close()

ADJ_TL_file = open(path_to_folder + "ADJ_TL.pkl", 'wb')
pickle.dump(ADJ_TL, ADJ_TL_file)
ADJ_TL_file.close()

TLEC_path_file = open(path_to_folder + "TLEC.pkl", 'wb')
pickle.dump(TLEC_Path, TLEC_path_file)
TLEC_path_file.close()

TLLC_path_file = open(path_to_folder + "TLLC.pkl", 'wb')
pickle.dump(TLLC_Path, TLLC_path_file)
TLLC_path_file.close()

save_5D_in_file("TLEC.txt", TLEC_Path)
save_5D_in_file("TLLC.txt", TLLC_Path)

print("TLEC paths are: ")
PRINT_TLEC_PATH_FILE(TLEC_Path, TLLC_Path, Parent_TE, Spectrum_TE)