#Area of Deployment
minX = 0
maxX = 100
minY = 0
maxY = 100

# Simulation Time  ---- 1 plus
T = 5

#TTL Bound ----  1 plus
TTL = 5

# Message size
M = [20]

V = 6         # No of nodes including source, data mules, and data centers
NoOfSources = 1
NoOfDMs = 5                 # Total number of data mules (or DSA nodes)
NoOfDataCenters = 1

VMIN = 1                    # Minimum Data Mule speed possible
VMAX = 10                   # Maximum Data mule speed possible

S = 3                       # Number of spectrum bands
minBW = [3, 10, 40]               # Minimum bandwidth for each spectrum band
maxBW = [6, 20, 60]             # Maximum bandwidth for each spectrum band
spectRange = [1, 2, 0.5]        # Transmission coverage for each spectrum band
spectPower = [1, 1, 1]          # Transmission power for each spectrum band
epsilon = 0