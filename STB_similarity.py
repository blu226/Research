import pickle


# V = 19
T = 180
S = 4
max_tau = 20

num_nodes = 18
day = "2007-11-06"

LE_path = "Bands_UMass" + str(num_nodes) + "/" + day + "/"

LE_path1 = LE_path + "Day1/LINK_EXISTS.pkl"
LE_path2 = LE_path + "Day2/LINK_EXISTS.pkl"

LINK_EXISTS1 = pickle.load(open(LE_path1, "rb"))
LINK_EXISTS2 = pickle.load(open(LE_path2, "rb"))



for V in range(num_nodes,8,-2):

    sim_links = 0
    total_links = 0

    for i in range(V):
        for j in range(V):
            for s in range(S):
                for ts in range(T):
                    end_time = ts + max_tau

                    if end_time >= 180:
                        end_time = 179

                    for te in range(ts + 1, end_time):

                        if LINK_EXISTS1[i,j,s,ts,te] == 1:
                            total_links += 1

                            if LINK_EXISTS2[i,j,s,ts,te] == 1:
                                sim_links += 1

    print("Similarity", V, ":", str((sim_links)/total_links), "sim Links:",sim_links, "total Links:", total_links)