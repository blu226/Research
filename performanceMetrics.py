import math
import pickle
import os
from constants import *

def print4D(adj):
    for i in range(len(adj)):
        for j in range(len(adj[0])):
            for t in range(len(adj[0][0])):
                for m in range(len(adj[0][0][0])):
                    print(str(i) + " " + str(j) + " " + str(t) + " "  + str(m) + " = " + str(adj[i, j, t, m]))

def print5D(adj):
    for i in range(len(adj)):
        for j in range(len(adj[0])):
            for t in range(len(adj[0][0])):
                for dt in range(len(adj[0][0][0])):
                    for m in range(len(adj[0][0][0][0])):
                        print(str(i) + " " + str(j) + " " + str(t) + " " + str(dt) + " " + str(m) + " = " + str(adj[i, j, t, dt, m]))


#============== LLC functions ====================

def pdr_LLC(lat_mat):
    delivered = 0
    not_delivered = 0

    for u in range(0, NoOfSources):
        for v in range(NoOfDMs, NoOfDMs + NoOfDataCenters):
            for t in range(T):
                for m in range(len(M)):
                    if(lat_mat[u, v, t, m] != math.inf):
                        delivered += 1
                    else:
                        not_delivered += 1
    if delivered == 0:
        avg_pdr = 0
    else:
        avg_pdr = float(delivered / (delivered + not_delivered))
    print("Avg. PDR: " + str(avg_pdr))


def latency_LLC(lat_mat):
    total_latency = 0
    delivered_messages = 0
    worstcase_latency = -1

    for u in range(0, NoOfSources):
        for v in range(NoOfDMs, NoOfDMs + NoOfDataCenters):
            for t in range(T):
                for m in range(len(M)):

                    if lat_mat[u, v, t, m] != math.inf:
                        total_latency += lat_mat[u, v, t, m]
                        delivered_messages += 1
                        if worstcase_latency < lat_mat[u, v, t, m]:
                            worstcase_latency = lat_mat[u, v, t, m]

    if delivered_messages == 0:
        avg_latency = 0
    else:
        avg_latency = float(total_latency/delivered_messages)
    print("Avg latency: " + str(avg_latency) + " Worst case latency: " + str(worstcase_latency))


def energy_LLC(energy_mat):
    total_energy = 0
    delivered_messages = 0

    for u in range(0, NoOfSources):
        for v in range(NoOfDMs, NoOfDMs + NoOfDataCenters):
            for t in range(T):
                for m in range(len(M)):
                    if (energy_mat[u, v, t, m] != math.inf):
                        total_energy += energy_mat[u, v, t, m]
                        delivered_messages += 1

    if delivered_messages == 0:
        avg_energy = 0
    else:
        avg_energy = float(total_energy / delivered_messages)
    print("Avg. Energy: "  + str(avg_energy))

#================= TLEC functions=======================

def pdr_TLEC(lat_mat):
    delivered = 0
    not_delivered = 0

    for u in range(0, NoOfSources):
        for v in range(NoOfDMs, NoOfDMs + NoOfDataCenters):
            for t in range(T):
                for m in range(len(M)):
                    if(lat_mat[u, v, t, TTL - 1, m] != math.inf):
                        delivered += 1
                    else:
                        not_delivered += 1

    if delivered == 0:
        avg_pdr = 0
    else:
        avg_pdr = float(delivered/(delivered + not_delivered))
    print("Avg. PDR: "  + str(avg_pdr))

def latency_TLEC(lat_mat):
    total_latency = 0
    delivered_messages = 0
    worstcase_latency = -1

    for u in range(0, NoOfSources):
        for v in range(NoOfDMs, NoOfDMs + NoOfDataCenters):
            for t in range(T):
                for m in range(len(M)):
                    if lat_mat[u, v, t, TTL - 1, m] < math.inf:
                        total_latency += lat_mat[u, v, t, TTL - 1, m]
                        delivered_messages += 1
                        if worstcase_latency < lat_mat[u, v, t, TTL - 1, m]:
                            worstcase_latency = lat_mat[u, v, t, TTL - 1, m]

    if delivered_messages == 0:
        avg_latency = 0
    else:
        avg_latency = float(total_latency/delivered_messages)
    print("Avg latency: " + str(avg_latency) + " Worst case latency: " + str(worstcase_latency))


def energy_TLEC(energy_mat):
    total_energy = 0
    delivered_messages = 0

    for u in range(0, NoOfSources):
        for v in range(NoOfDMs, NoOfDMs + NoOfDataCenters):
            for t in range(T):
                for m in range(len(M)):
                    if (energy_mat[u, v, t, TTL - 1, m] != math.inf):
                        total_energy += energy_mat[u, v, t, TTL - 1, m]
                        delivered_messages += 1

    if delivered_messages == 0:
        avg_energy = 0
    else:
        avg_energy = float(total_energy / delivered_messages)
    print("Avg energy: " + str(avg_energy))


band_types = ["ALL", "TV"]

print("#================ For LLC paths===========")

for i in range(len(band_types)):
    local_path_to_folder = "Bands/"  + band_types[i] + "/"

    print("\nSpectrum: ", band_types[i])
   # if os.path.isfile(local_path_to_folder + latency_files[ind]):
    latency_file = pickle.load(open(local_path_to_folder + "LLC.pkl", "rb"))
    energy_file = pickle.load(open(local_path_to_folder + "ELC.pkl", "rb"))

    # print4D(latency_file)

    pdr_LLC(latency_file)
    latency_LLC(latency_file)
    energy_LLC(energy_file)


print("\n\n#================ For TLEC paths===========")

for i in range(len(band_types)):
    local_path_to_folder = "Bands/"  + band_types[i] + "/"

    print("\nSpectrum: ", band_types[i])
   # if os.path.isfile(local_path_to_folder + latency_files[ind]):
    latency_file = pickle.load(open(local_path_to_folder + "TLLC.pkl", "rb"))
    energy_file = pickle.load(open(local_path_to_folder + "TLEC.pkl", "rb"))

    # print5D(latency_file)

    pdr_TLEC(latency_file)
    latency_TLEC(latency_file)
    energy_TLEC(energy_file)

