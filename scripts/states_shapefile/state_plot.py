from __future__ import division

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.collections import LineCollection
from mpl_toolkits.basemap import Basemap, cm

# from shapelib import ShapeFile
# import dbflib

# shapefiles from http://nationalatlas.gov/atlasftp.html?openChapters=chpbound

fig = plt.figure(figsize=(12, 12))
ax = fig.add_axes([0.1,0.1,0.8,0.8])
lllat = 21; urlat = 53; lllon = -118; urlon = -62

m = Basemap(ax=ax, projection='stere',
    lon_0=(urlon + lllon) / 2, lat_0=(urlat + lllat) / 2, llcrnrlat=lllat,
    urcrnrlat=urlat, llcrnrlon=lllon, urcrnrlon=urlon, resolution='l')
m.drawcoastlines()
m.drawcountries()
m.readshapefile('statep010', 'shp')
