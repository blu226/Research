#Area of Deployment

#Only for sample graphs
minX = 0
maxX = 100
minY = 0
maxY = 100

#Required to generate lexington synthetic data
VMIN = 30000                    # Minimum Data Mule speed (in m/s)
VMAX = 50000                   # Maximum Data mule speed (in m/s)

#Required in readLexingtonData, computeLINKEXISTS, and STB_Main_Graph - to create the STB graph
lex_data_directory = "Lexington/Day1/"

#Only required for main2.py to validate the created STB graph for different day
validate_data_directory = "Lexington/Day1/"

# validate_data_directory = "Data/"
delivery_file_name = "delivery_day1.txt"

# Start times may be different for different buses
route_start_time1 = 0
route_start_time2 = 10

# Simulation Time  ---- 1 plus
T = 20   # must be greater than start time
dt = 1  # this is the discrete time interval such as 0, 2, 4, 6, 8, ...
tau = 1 # Instead of looking at each dt, we would look at tau as this is the minimum time to transfer a message

#TTL Bound ----  1 plus
TTL = 20

#max tau is the time taken to deliver the maximum size message over slowest band (with least bandwidth)
maxTau = 5
# Message size
M = [20]

V = 40         # No of nodes including source, data mules, and data centers
NoOfSources = 5
NoOfDataCenters = 5
NoOfDMs = 30                # Total number of data mules (or DSA nodes)



# path_to_folder = "Bands/ALL/"  #for all spectrum types
# path_to_folder = "Bands/TV/"  #for all spectrum types
# path_to_folder = "Bands/ISM/"  #for all spectrum types
path_to_folder = "Bands/ALL/"  #for all spectrum types
# path_to_folder = "Bands/Sample5/" #For sample graph with 4 nodes

numSpec = 3 #always even if we only use one band

S = [0, 1, 2]                      # Number of spectrum bands
#3, 10, 40
minBW = [3, 10, 20]               # Minimum bandwidth for each spectrum band
#6, 20, 60
maxBW = [6, 20, 30]             # Maximum bandwidth for each spectrum band
#2000, 100, 500
spectRange = [2000, 300, 500]        # Transmission coverage for each spectrum band
# specRange = [1, 2, 0.5]
spectPower = [1, 1, 1]          # Transmission power for each spectrum band

epsilon = 0             #energy consumed in temporal link



#Message generation
lambda_val = 1   #lambda in exponential function
messageBurst = [2, 5]


