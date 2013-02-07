import pandas as pd
import matplotlib.pyplot as plt

# Change path to local version.
s = pd.HDFStore('/Volumes/HDD/Users/tom/DataStorage/Patents/patents.h5')

df = s['utility']

## Counts by year
gr = df.groupby(df['gyear'])
fig = gr['patent'].count().plot(rot=45)
