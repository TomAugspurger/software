from __future__ import division

import matplotlib

matplotlib.use("AGG")
"""
Files available from:
https://sites.google.com/site/patentdataproject/Home/downloads

Directly:
http://www.nber.org/~jbessen/patassg.dat.zip
http://www.nber.org/~jbessen/pat76_06_assgasc.zip
"""

import numpy as np
import pandas as pd
from pandas.io.data import DataReader
import matplotlib.pyplot as plt
from patent_lookup import Lookup
# Change path to local version.
s = pd.HDFStore('/Volumes/HDD/Users/tom/DataStorage/Patents/patents.h5')

df = s['utility']

cat = df['subcat']
t = df[(cat == 22.0) | (cat == 24.0) | (cat == 25.0)]
# To adjust for population
try:
    popn = DataReader('CNP16OV', data_source='fred', start='1970')
    popn = popn.resample('A')
    gdp = DataReader('GDPC1', data_source='fred',
                     start='1974').resample('A')
except IOError:
    print('No Connection.')

patents = df.groupby('appyear')['patent'].count().ix[1975:2002]
gdp = gdp.ix['1975':'2002']
patents.index = gdp.index
gdp['patents'] = patents
gdp.rename(columns={'GDPC1': 'gdp'})
fig = plt.figure()
ax = fig.add_subplot(111)
ax = gdp.plot(ax=ax, secondary_y=['patents'], grid=True)
ax.set_ylabel('Billions of Chained 2005 Dollars')
ax.set_xlabel('')
plt.savefig('gdp_app_all.png', dpi=300)

patents = t.groupby('appyear')['patent'].count().ix[1975:2002]
gdp = gdp.ix['1975':'2002']
patents.index = gdp.index
gdp['patents'] = patents
gdp.rename(columns={'GDPC1': 'gdp'})
fig = plt.figure()
ax = fig.add_subplot(111)
ax = gdp.plot(ax=ax, secondary_y=['patents'], grid=True)
ax.set_ylabel('Billions of Chained 2005 Dollars')
ax.set_xlabel('')
plt.savefig('gdp_app_tech.png', dpi=300)
