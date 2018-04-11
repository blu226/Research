#Area of Deployment
minX = 0
maxX = 100
minY = 0
maxY = 100
route_start_time1 = 0
route_start_time2 = 60 # start times may be different for different routes

# Simulation Time  ---- 1 plus
T = 10
dt = 1  # this is the discrete time interval such as 0, 2, 4, 6, 8, ...
tau = 1 # Instead of looking at each dt, we would look at tau as this is the minimum time to transfer a message

#TTL Bound ----  1 plus
TTL = 8

# Message size
M = [20]

V = 30         # No of nodes including source, data mules, and data centers
NoOfSources = 5
NoOfDMs = 20                # Total number of data mules (or DSA nodes)
NoOfDataCenters = 5

VMIN = 20000                    # Minimum Data Mule speed (in m/s)
VMAX = 50000                   # Maximum Data mule speed (in m/s)

S = 3                       # Number of spectrum bands
minBW = [3, 10, 40]               # Minimum bandwidth for each spectrum band
maxBW = [6, 20, 60]             # Maximum bandwidth for each spectrum band
spectRange = [2000, 300, 100]        # Transmission coverage for each spectrum band
# specRange = [1, 2, 0.5]
spectPower = [1, 1, 1]          # Transmission power for each spectrum band
epsilon = 0