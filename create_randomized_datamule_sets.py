from STB_help import *
import random

def get_random_files(num_nodes, num_combinations, total_nodes):

    combination_list = []

    for i in range(num_combinations):

        random_set_of_mules = []

        for j in range(num_nodes):

            rand_ind = random.randint(0, total_nodes)

            while rand_ind in random_set_of_mules:
                rand_ind = random.randint(0, total_nodes)

            random_set_of_mules.append(rand_ind)

        random_set_of_mules.sort()



total_nodes = 10
num_nodes = 6
num_combinations = 8

day_string = "2007-11-06"
main_dataMule_path = "DataMules/" + day_string + "/"
all_dataMules = findfiles(main_dataMule_path)

