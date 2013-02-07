import pandas as pd

# Change path to local version.
s = pd.HDFStore('/Volumes/HDD/Users/tom/DataStorage/Patents/patents.h5')

df = s['utility']

## Counts by year
gr = df.groupby(df['appyear'])
fig = gr['patent'].count().plot(kind='bar')
