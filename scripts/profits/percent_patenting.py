"""
1. What percent of all companies in my wrds set are patenting?

2. What percent of companies (in wrds) who are researching are patenting?
"""
from __future__ import division, print_function, unicode_literals

import pandas as pd

s = pd.HDFStore('/Volumes/HDD/Users/tom/DataStorage/Patents/patents.h5')

companies = pd.read_csv(
    '/Volumes/HDD/Users/tom/DataStorage/Patents/dynass.dat',
    sep='\t', index_col='pdpass')

df = s['utility']

ind = companies.index
pdp = pd.unique(df.pdpass)

print(companies.index.is_unique)

inter = ind.intersection(pdp)

print('The ratio is {}.'.format(len(inter) / len(ind)))
gv_pats = companies[['gvkey1', 'gvkey2', 'gvkey3', 'gvkey4', 'gvkey5']]
gv_pats = pd.unique(gv_pats.values.ravel())
# Now bring in compustat

rd = s.select('profit')
gv_comp = rd.index.levels[0]

# Question 1:
print('Number from patents: {0},\n number from compustat: {1}\n Ratio of firms patenting = {2}'.format(len(gv_pats), len(gv_comp),
      len(gv_pats) / len(gv_comp)))
# Number from patents: 7770,
# number from compustat: 23317
# Ratio of firms patenting = 0.333233263284


# Question 2.
gv_comp = set(x[0] for x in rd.xrdq.dropna().index)
print(('Number from patents: {0},\n number from compustat:' +
       '{1}\n Ratio of firms patenting = {2}').format(
            len(gv_pats), len(gv_comp), len(gv_pats) / len(gv_comp)))

# Number from patents: 7770,
# number from compustat:9966
# Ratio of firms patenting = 0.779650812763
