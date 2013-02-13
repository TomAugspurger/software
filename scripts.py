"""
Files available from:
https://sites.google.com/site/patentdataproject/Home/downloads

Directly:
http://www.nber.org/~jbessen/patassg.dat.zip
http://www.nber.org/~jbessen/pat76_06_assgasc.zip
"""

import pandas as pd
import matplotlib.pyplot as plt
try:
    from mpl_toolkits import basemap
except ImportError:
    print('Won\'t be able to plot the maps.')

# Change path to local version.
s = pd.HDFStore('/Volumes/HDD/Users/tom/DataStorage/Patents/patents.h5')

df = s['utility']

## Counts by year
gr = df.groupby(df['gyear'])
fig = gr['patent'].count().plot(rot=45)
fig.set_xlabel('Year')
fig.set_ylabel('Patents')

## Claims per year?  Not really. lag.
plt.figure()
fig2 = (gr['nclaims'].sum() / gr['patent'].count()).plot()
fig2.set_xlabel('Year')
fig2.set_ylabel('Claims per Patent?')

## Patents by Country
by_ctry = df.groupby('country')['patent'].count()
by_ctry.sort()
fig3 = by_ctry[-10:].plot(kind='barh')
fig3.set_ylabel('Patents')


## By Country and time.
by_ctry_time = df.groupby(['country', 'gyear'])['patent'].count()
idx = by_ctry[-10:].index
by_ctry_time = by_ctry_time.ix[idx]
by_ctry_time.index = by_ctry_time.index.swaplevel(1, 0)
fig4 = (by_ctry_time.unstack()).plot()
fig.set_xlabel('Year')
fig.set_ylabel('Patents')

## Experiments with basemap and shapefiles
# Requires http://matplotlib.org/basemap/users/installing.html
# Which relies on a C library.
"""
Doc Dump:

State map from: http://www.arcgis.com/home/item.html?id=f7f805eb65eb4ab787a0a3e1116ca7e5
matplotlib examples: http://matplotlib.org/basemap/users/examples.html
filling: http://www.geophysique.be/2011/01/27/matplotlib-basemap-tutorial-07-shapefiles-unleached/
http://matplotlib.1069221.n5.nabble.com/How-to-draw-a-specific-country-by-basemap-td15744.html
http://www.naturalearthdata.com
"""


gr = df.groupby('state')
cts = gr['patent'].count()
