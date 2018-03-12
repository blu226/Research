#Area of Deployment
minX = 0
maxX = 100
minY = 0
maxY = 100

# Simulation Time
T = 5

#TTL Bound
TTL = 4

# Message size
M = [20]

V = 5          # No of nodes including source, data mules, and data centers
NoOfSources = 1
NoOfDMs = 3                 # Total number of data mules (or DSA nodes)
NoOfDataCenters = 1

VMIN = 1                    # Minimum Data Mule speed possible
VMAX = 10                   # Maximum Data mule speed possible

S = 3                       # Number of spectrum bands
minBW = [20, 20, 20]               # Minimum bandwidth for each spectrum band
maxBW = [25, 25, 25]             # Maximum bandwidth for each spectrum band
spectRange = [5, 10, 15]        # Transmission coverage for each spectrum band
spectPower = [1, 1, 1]          # Transmission power for each spectrum band
epsilon = 0