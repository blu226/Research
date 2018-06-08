import os

directory = "Bands/"
folders = os.listdir(directory)
folders.sort()

for day in folders:

    path1 = "./Bands/" + day + "/specBW.txt "
    path2 = "/localdisk1/SCRATCH/epidemic/Bands_UMass/" + day

    command = "cp " + path1 + path2

    os.system(command)