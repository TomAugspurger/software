import pandas as pd
import matplotlib.pyplot as plt

# Change path to local version.
s = pd.HDFStore('/Volumes/HDD/Users/tom/DataStorage/Patents/patents.h5')

df = s['utility']

## Counts by year
gr = df.groupby(df['gyear'])
fig = gr['patent'].count().plot(rot=45)

## Claims per year?  Not really. lag.
plt.figure()
(gr['nclaims'].sum() / gr['patent'].count()).plot()

## Patents by Country
by_ctry = df.groupby('country')['patent'].count()
by_ctry.sort()
fig = by_ctry[-10:].plot(kind='barh')

## By Country and time.
by_ctry_time = df.groupby(['country', 'gyear'])['patent'].count()
idx = by_ctry[-10:].index
by_ctry_time = by_ctry_time.ix[idx]
by_ctry_time.index = by_ctry_time.index.swaplevel(1, 0)
(by_ctry_time.unstack()).plot()
