from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

map = Basemap(projection='merc', 
			resolution = 'h', 
			llcrnrlon = -72.5293, 
			llcrnrlat = 42.3014, 
			urcrnrlon = -72.4895, 
			urcrnrlat = 42.4333)


map.drawcoastlines()
map.drawstates()
#map.fillcontinents(color='coral')
#map.drawmapboundary()

lons = [-72.496819]
lats = [42.340382]
x,y = map(lons, lats)
map.plot(x, y, 'bo', markersize=18)

plt.show()