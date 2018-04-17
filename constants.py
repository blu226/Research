#Area of Deployment

#Only for sample graphs
minX = 0
maxX = 100
minY = 0
maxY = 100

#Required to generate lexington synthetic data
VMIN = 20000                    # Minimum Data Mule speed (in m/s)
VMAX = 50000                   # Maximum Data mule speed (in m/s)

lex_data_directory = "Lexington/Day2/"
delivery_file_name = "delivery_day2.txt"
# Start times may be different for different buses
route_start_time1 = 0
route_start_time2 = 2

# Simulation Time  ---- 1 plus
T = 11   # must be greater than start time
dt = 1  # this is the discrete time interval such as 0, 2, 4, 6, 8, ...
tau = 1 # Instead of looking at each dt, we would look at tau as this is the minimum time to transfer a message

#TTL Bound ----  1 plus
TTL = 5

# Message size
M = [20]

V = 15         # No of nodes including source, data mules, and data centers
NoOfSources = 3
NoOfDataCenters = 2
NoOfDMs = 10                # Total number of data mules (or DSA nodes)



path_to_folder = "Bands/ALL/"  #for all spectrum types
# path_to_folder = "Bands/TV/"  #for all spectrum types
# path_to_folder = "Bands/ISM/"  #for all spectrum types
# path_to_folder = "Bands/Sample5/" #For sample graph with 4 nodes

S = 3                      # Number of spectrum bands
#3, 10, 40
minBW = [3, 10, 40]               # Minimum bandwidth for each spectrum band
#6, 20, 60
maxBW = [6, 20, 60]             # Maximum bandwidth for each spectrum band
#2000, 100, 500
spectRange = [2000, 100, 500]        # Transmission coverage for each spectrum band
# specRange = [1, 2, 0.5]
spectPower = [1, 1, 1]          # Transmission power for each spectrum band

epsilon = 0             #energy consumed in temporal link

