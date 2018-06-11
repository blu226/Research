import math
import pickle

path_to_folder = 'Bands15/3/Day1/ALL/'
link_exists_folder = 'Bands15/3/Day1/'

specBW = pickle.load(open("Bands15/3/Day1/specBW.pkl", "rb"))

fx = open(path_to_folder + "delivery_day1.txt", "r")
xLines = fx.readlines()[2:]
fx.close()

fe = open(path_to_folder + "unique_epidemic_messages.txt", "r")
eLines = fe.readlines()[2:]
fe.close()

fl_path = open(path_to_folder + "LLC_PATH.txt")
llc_path_lines = fl_path.readlines()[1:]
fl_path.close()

fl_spec = open(path_to_folder + "LLC_Spectrum.txt")
llc_spec_lines = fl_spec.readlines()[1:]
fl_spec.close()

ft_time = open(path_to_folder + "LLC_time.txt")
llc_time_lines = ft_time.readlines()[1:]
ft_time.close()

fc = open(path_to_folder + "xchants_epidemic.txt", "w")

str_line = "ID\ts\td\tt\tm\tLLC\tXchants\tEpidemic"
fc.write(str_line + "\n")
fc.write("---------------------------------\n")

print(str_line)

#Read each file, and see the difference
for ind in range(len(llc_path_lines)):
    ll_path_arr = llc_path_lines[ind].strip().split("\t")
    ll_spec_arr = llc_spec_lines[ind].strip().split("\t")
    ll_time_arr = llc_time_lines[ind].strip().split("\t")
    for xl in xLines:
        xl_arr = xl.strip().split("\t")
        for el in eLines:
            el_arr = el.strip().split("\t")

            # print(ll_path_arr[4] + "\t" + xl_arr[6] + "\t" + el_arr[5] + "\n")

            #condition i == s, j == d, t == ts, and m = size
            if  ll_path_arr[0] == xl_arr[1] and xl_arr[1] == el_arr[1] and \
                ll_path_arr[1] == xl_arr[2] and xl_arr[2] == el_arr[2] and \
                ll_path_arr[2] == xl_arr[3] and xl_arr[3] == el_arr[3] and \
                ll_path_arr[3] == xl_arr[5] and xl_arr[5] == el_arr[6]:

                s_d_t_m = xl_arr[0] +"\t" + ll_path_arr[0]+"\t" + ll_path_arr[1] + "\t" + ll_path_arr[2] + "\t" + ll_path_arr[3] +" : "
                llc_xchants_epidemic = ll_path_arr[4] +"\t" + xl_arr[6] + "\t" + el_arr[5]

                #If latency costs are different
                if ll_path_arr[4] != xl_arr[6] or ll_path_arr[4] != el_arr[5] or xl_arr[6] != el_arr[5]:
                    fc.write(s_d_t_m + "\t" + llc_xchants_epidemic + "\n")
                    print(s_d_t_m + "\t" + llc_xchants_epidemic)
                    print("Path: ", ll_path_arr[5:])
                    print("Spec: ", ll_spec_arr[5:])
                    print("Time: ", ll_time_arr[5:])

                    # fc.write("Path: " + str(ll_path_arr[5:]) +"\n")
                    # fc.write("Spec: " + str(ll_spec_arr[5:]) + "\n\n")
                    path = ll_path_arr[5:]
                    spec = ll_spec_arr[5:]

                    BW_arr =[]
                    consTime_arr = []

                    curr_time =  int(ll_path_arr[2])
                    for i in range(len(path)-1, 0, -1):
                        j = i - 1

                        # if int(spec[j]) > 4:
                        #     BW_arr.insert(0, 1)
                        #     consTime_arr.insert(0, 1)
                        #     curr_time += 1


                        consTime = math.ceil(int(ll_path_arr[3])/specBW[int(path[i]), int(path[j]), int(spec[j])%10 - 1, curr_time])
                        consTime_arr.insert(0, consTime)
                        BW_arr.insert(0, specBW[
                            int(path[i]), int(path[j]), int(spec[j])%10 - 1, curr_time])

                        curr_time += consTime

                    print("BW: ", BW_arr)
                    print("LLC: ", consTime_arr, " Tot: ", sum(consTime_arr) , "\n")

fc.close()



