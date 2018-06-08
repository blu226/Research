from math import radians, cos, sin, asin, sqrt, inf



def funHaversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    #print("lon1: " + str(lon1) + " lat1: " + str(lat1) + " lon2: " + str(lon2) + " lat2: " + str(lat2) )

    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    # Radius of earth in kilometers is 6371
    m = 6371* c * 1000
    # print(" dist: " + str(km))
    return m

#top left
lat1 = 42.378161
lon1 = -72.633090
#bottom left
lat2 = 42.249248
lon2 = -72.622827
#bottom right
lat3 = 42.265221
lon3 = -72.472817

#print distances to get dimensions of UMass bus routes
dist1 = funHaversine(lon1, lat1, lon2, lat2)
#dist2 = funHaversine(lon1, lat1, lon3, lat3)
dist3 = funHaversine(lon2, lat2, lon3, lat3)

#print(str(dist1/1000) + " "  + str(dist3/1000))

