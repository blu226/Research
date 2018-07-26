import numpy as np
import matplotlib.pyplot as plt



time_epochs = 8
runs = 3

Xchants = np.zeros(shape=(time_epochs, runs))
Xchants_pk = np.zeros(shape=(time_epochs, runs))
Epidemic_ALL = np.zeros(shape=(time_epochs, runs))
Epidemic_LTE = np.zeros(shape=(time_epochs, runs))
Epidemic_TV = np.zeros(shape=(time_epochs, runs))
Epidemic_CBRS = np.zeros(shape=(time_epochs, runs))
Epidemic_ISM = np.zeros(shape=(time_epochs, runs))
SprayNWait_ALL = np.zeros(shape=(time_epochs, runs))
HotPotato_ALL = np.zeros(shape=(time_epochs, runs))



days = [ "2007-11-01", "2007-11-07", "2007-11-06"]
# days = ["2007-11-06"]

folder_nums = [19]
bands = ["ALL", "LTE", "TV", "CBRS", "ISM"]
protocols = ["XChants", "Epidemic", "SprayNWait", "HotPotato"]

p_id = 1 # p_id = 1 for PDR, = 2 for latency, and 3 for Energy, and 4 for overhead


#Get Data from metrics files
for num_mules in folder_nums:
    for i in range(runs):
        directory = "../Bands_UMass" + str(num_mules) + "/" + days[i] + "/Day2/"

        for band in bands:
            directory_band = directory + band + "/"

            for protocol in protocols:

                directory_band_proto = directory_band + protocol + "/"

                if protocol == "XChants":
                    metrics_file = "metrics_LLC_day2_X-CHANTS.txt"
                elif protocol == "Epidemic":
                    metrics_file = "metrics_LLC_day2_Epi.txt"
                elif protocol == "SprayNWait":
                    metrics_file = "metrics_LLC_day2_SnW.txt"
                elif protocol == "HotPotato":
                    metrics_file = "metrics_LLC_day2_HP.txt"

                if band == "ALL" or protocol == "Epidemic":
                    with open(directory_band_proto + metrics_file) as f:
                        lines = f.readlines()[2:]

                    t = 0

                    for line in lines:
                        line_arr = line.strip().split()

                        if line_arr[p_id] == "None":
                            line_arr[p_id] = 0

                        if "XChants" == protocol:
                            if "ALL" == band:
                                Xchants[t][i] = line_arr[p_id]

                        elif "Epidemic" == protocol:
                            if "ALL" == band:
                                Epidemic_ALL[t][i] = line_arr[p_id]
                            elif "LTE" == band:
                                Epidemic_LTE[t][i] = line_arr[p_id]
                            elif "TV" == band:
                                Epidemic_TV[t][i] = line_arr[p_id]
                            elif "CBRS" == band:
                                Epidemic_CBRS[t][i] = line_arr[p_id]
                            elif "ISM" == band:
                                Epidemic_ISM[t][i] = line_arr[p_id]

                        elif "SprayNWait" == protocol:
                            if "ALL" == band:
                                SprayNWait_ALL[t][i] = line_arr[p_id]

                        elif "HotPotato" == protocol:
                            if "ALL" == band:
                                HotPotato_ALL[t][i] = line_arr[p_id]
                        t += 1

time = 0
for num_mules in folder_nums:
    for i in range(runs):
        t = 0
        metric_file = open("../Bands_UMass" + str(num_mules) +"/" + days[i] + "/Day2/ALL/XChants/metrics_LLC_day2_X-CHANTS_opt.txt", "r")
        lines = metric_file.readlines()[2:]
        for line in lines:
            line_arr = line.strip().split("\t")
            Xchants_pk[t][i] = line_arr[p_id]
            t += 1

if p_id == 3:
    for t in range(len(Xchants)):
        for run in range(runs):
            Xchants[t][run] = float(Xchants[t][run]) / 1000
            Xchants_pk[t][run] = float(Xchants_pk[t][run])/1000
            Epidemic_ALL[t][run] = float(Epidemic_ALL[t][run]) / 1000
            Epidemic_TV[t][run] = float(Epidemic_TV[t][run]) / 1000
            Epidemic_LTE[t][run] = float(Epidemic_LTE[t][run]) / 1000
            Epidemic_ISM[t][run] = float(Epidemic_ISM[t][run]) / 1000
            Epidemic_CBRS[t][run] = float(Epidemic_CBRS[t][run]) / 1000
            SprayNWait_ALL[t][run] = float(SprayNWait_ALL[t][run])/1000
            HotPotato_ALL[t][run] = float(HotPotato_ALL[t][run])/1000

Xchants_mean = []
Xchants_SD = []
Xchants_mean_pk = []
Xchants_SD_pk = []
Epidemic_ALL_mean = []
Epidemic_ALL_SD = []
Epidemic_CBRS_mean = []
Epidemic_CBRS_SD = []
Epidemic_ISM_mean = []
Epidemic_ISM_SD = []
Epidemic_LTE_mean = []
Epidemic_LTE_SD = []
Epidemic_TV_mean = []
Epidemic_TV_SD = []
SprayNWait_ALL_mean = []
SprayNWait_ALL_SD = []
HotPotato_ALL_mean = []
HotPotato_ALL_SD = []

for i in range(len(Xchants)):
    Xchants_mean.append(np.mean(Xchants[i]))
    Xchants_SD.append(np.std(Xchants[i]))
    Xchants_mean_pk.append(np.mean(Xchants_pk[i]))
    Xchants_SD_pk.append(np.std(Xchants_pk[i]))
    SprayNWait_ALL_mean.append(np.mean(SprayNWait_ALL[i]))
    SprayNWait_ALL_SD.append(np.std(SprayNWait_ALL[i]))
    HotPotato_ALL_mean.append(np.mean(HotPotato_ALL[i]))
    HotPotato_ALL_SD.append(np.std(HotPotato_ALL[i]))
    Epidemic_ALL_mean.append(np.mean(Epidemic_ALL[i]))
    Epidemic_ALL_SD.append(np.std(Epidemic_ALL[i]))
    Epidemic_CBRS_mean.append(np.mean(Epidemic_CBRS[i]))
    Epidemic_CBRS_SD.append(np.std(Epidemic_CBRS[i]))
    Epidemic_ISM_mean.append(np.mean(Epidemic_ISM[i]))
    Epidemic_ISM_SD.append(np.std(Epidemic_ISM[i]))
    Epidemic_LTE_mean.append(np.mean(Epidemic_LTE[i]))
    Epidemic_LTE_SD.append(np.std(Epidemic_LTE[i]))
    Epidemic_TV_mean.append(np.mean(Epidemic_TV[i]))
    Epidemic_TV_SD.append(np.std(Epidemic_TV[i]))

#Create plot
x = np.array([30, 60, 90, 120, 150, 180])
plt.xticks(fontsize=25)
plt.yticks(fontsize=25)
plt.xticks(np.arange(30, 190,step=30))
# plt.xlim(0,12)
fig_name = "dummy.eps"

if p_id == 1:
    plt.ylabel('Message delivery ratio', fontsize=25)
    plt.xlabel('Time (min)', fontsize=25)
    # plt.ylim(0,1.15)
    fig_name = "../Plots/pdr_time_UMass.eps"

if p_id == 2:
    plt.ylabel('Latency (min)', fontsize=25)
    plt.xlabel('Time (min)', fontsize=25)

    fig_name = "../Plots/latency_time_UMass.eps"

if p_id == 3:
    plt.ylabel('Energy Expenditure (KJ)', fontsize=25)
    plt.xlabel('Time (min)', fontsize=25)
    plt.ylim(0, 30)
    fig_name = "../Plots/energy_time_UMass.eps"

if p_id == 4:
    plt.ylabel('Message overhead', fontsize=25)
    plt.xlabel('Time (min)', fontsize=25)
    plt.ylim(0, 85)
    fig_name = "../Plots/overhead_time_UMass.eps"


plt.errorbar(x, Epidemic_CBRS_mean[:6], 0, marker='*', linestyle='-.', linewidth=2)
plt.errorbar(x, Epidemic_ISM_mean[:6], 0, marker='*', linestyle='-.', linewidth=2)
plt.errorbar(x, Epidemic_LTE_mean[:6], 0, marker='*', linestyle='-.', linewidth=2)
plt.errorbar(x, Epidemic_TV_mean[:6], 0, marker='*', linestyle='-.', linewidth=2)
plt.errorbar(x, Epidemic_ALL_mean[:6], 0, marker='*', linestyle='-.', linewidth=2)
plt.errorbar(x, SprayNWait_ALL_mean[:6], 0, marker='D', linestyle='--', linewidth=2)
plt.errorbar(x, HotPotato_ALL_mean[:6], 0, marker='^', linestyle='--', linewidth=2)
plt.errorbar(x, Xchants_mean[:6], 0, marker='o', linestyle='-', linewidth=2, color="#813a5c")
plt.errorbar(x, Xchants_mean_pk[:6], 0, marker='o', linestyle='--', linewidth=2, color="#49FF00")

# plt.errorbar(x, Xchants_mean_pk, Xchants_SD_pk, marker='o', linestyle='-', linewidth=2)
# plt.errorbar(x, Xchants_mean, Xchants_SD, marker='o', linestyle='-', linewidth=2)
# plt.errorbar(x, Epidemic_ALL_mean, Epidemic_ALL_SD, marker='*', linestyle='--', linewidth=2)
# plt.errorbar(x, Epidemic_CBRS_mean, Epidemic_CBRS_SD, marker='*', linestyle=':', linewidth=2)
# plt.errorbar(x, Epidemic_ISM_mean, Epidemic_ISM_SD, marker='*', linestyle='--', linewidth=2)
# plt.errorbar(x, Epidemic_LTE_mean, Epidemic_LTE_SD, marker='*', linestyle='--', linewidth=2)
# plt.errorbar(x, Epidemic_TV_mean, Epidemic_TV_SD, marker='*', linestyle='--', linewidth=2)
# plt.errorbar(x, SprayNWait_ALL_mean, SprayNWait_ALL_SD, marker='D', linestyle='--', linewidth=2, color="#813a5c")
# plt.errorbar(x, HotPotato_ALL_mean, HotPotato_ALL_SD, marker='^', linestyle='--', linewidth=2, color="#49FF00")

if p_id == 1:
    plt.legend([ "ER (CBRS)","ER (ISM)","ER (LTE)","ER (TV)", "S-ER ","S-SnW ", "S-HP",  "dDSAaR", "dDSAaR (Ideal)"], loc="center", bbox_to_anchor=(.7,0.3), fontsize=14, ncol = 2, frameon=False)
elif p_id == 2:
    plt.legend([ "ER (CBRS)","ER (ISM)","ER (LTE)","ER (TV)", "S-ER ","S-SnW ", "S-HP",  "dDSAaR", "dDSAaR (Ideal)"], loc="lower center", fontsize=14, ncol = 3, frameon=False)
elif p_id ==3:
    plt.legend([ "ER (CBRS)","ER (ISM)","ER (LTE)","ER (TV)", "S-ER ","S-SnW ", "S-HP", "dDSAaR", "dDSAaR (Ideal)"], loc="upper left", fontsize=14, ncol = 3, frameon=False)
elif p_id ==4:
    plt.legend([ "ER (CBRS)","ER (ISM)","ER (LTE)","ER (TV)", "S-ER ","S-SnW ", "S-HP", "dDSAaR", "dDSAaR (Ideal)"], loc="upper left", fontsize=14, ncol = 3, frameon=False)


plt.tight_layout()
plt.savefig(fig_name)

plt.show()

