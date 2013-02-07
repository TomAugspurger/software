import pandas as pd
import matplotlib.pyplot as plt

# Change path to local version.
s = pd.HDFStore('/Volumes/HDD/Users/tom/DataStorage/Patents/patents.h5')

df = s['utility']

## Counts by year
gr = df.groupby(df['appyear'])
fig = gr['patent'].count().plot(kind='bar', rot=45)
ticks = fig.get_xticks()
labels = fig.get_xticklabels()

p = 5  # Sparsity parameter
l2 = [str(x.get_text()) for x in labels[::p]]
fig.set_xticks(ticks[::p])
fig.set_xticklabels(l2)
plt.draw()
