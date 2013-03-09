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

import pandas as pd
import matplotlib.pyplot as plt

# Change path to local version.
s = pd.HDFStore('/Volumes/HDD/Users/tom/DataStorage/Patents/patents.h5')
df = s['utility']
df = df[df.duplicated('patent')]  # Drop the dupes for multiple assignees.
cat = df['subcat']
t = df[(cat == 22.0) | (cat == 24.0) | (cat == 25.0)]


def _get_ind(s, n=10):
    """Helper to get the top n countries.
    """
    s.sort()
    return s[-n:].index

by_ctry = df.groupby('country')['patent'].count()
t_by_ctry = t.groupby('country')['patent'].count()


idx = _get_ind(by_ctry)
t_idx = _get_ind(t_by_ctry)

comb = pd.DataFrame([by_ctry[idx], t_by_ctry[t_idx]]).T
comb.columns = ['All', 'Tech']

miss_all = comb[pd.isnull(comb['All'])].index
for ctry in miss_all:
    comb.ix[ctry]['All'] = df.groupby('country')['patent'].count().ix[ctry]

miss_tech = comb[pd.isnull(comb['Tech'])].index
for ctry in miss_tech:
    comb.ix[ctry]['Tech'] = t.groupby('country')['patent'].count().ix[ctry]

# This would be fun to animate. Composition may change though.  Needn't though.
ax = comb.plot(kind='barh', stacked=True)
ax.set_xlabel('Patents Granted')
plt.savefig('../resources/by_country.png', dpi=300)
normed = comb.div(comb.sum(1), axis=0)
ax2 = normed.plot(kind='barh', stacked=True)
ax2.set_xlabel('Proportion of Tech Patents')
plt.savefig('../resources/by_country_normalized.png', dpi=300)
