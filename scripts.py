"""
Files available from:
https://sites.google.com/site/patentdataproject/Home/downloads

Directly:
http://www.nber.org/~jbessen/patassg.dat.zip
http://www.nber.org/~jbessen/pat76_06_assgasc.zip
"""

import pandas as pd
import matplotlib.pyplot as plt

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
