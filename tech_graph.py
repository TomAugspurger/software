import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from networkx import graphviz_layout
from scipy import sparse

s = pd.HDFStore('/Volumes/HDD/Users/tom/DataStorage/Patents/patents.h5')
# ut = s['utility']
net = s['cites']

"""
Create two mappings from integers to patent numbers; one for citing, one
for cited.

I'm going back and forth on the need for sortedness here.  There is a meaning,
via the time a patent is granted and its number, but we'll probably be
breaking into groups anyway.  For now I say sort when possible.
"""
net.sort(columns='citing', inplace=True)
map_citing = pd.Series(net['citing'].unique())
net.sort(columns='cited', inplace=True)
map_cited = pd.Series(net['cited'].unique())

sp = sparse.lil_matrix((len(map_citing), len(map_cited)))  # Check other sparse fmts.
net.sort_index(inplace=True)  # Will speed the filling greatly I think.
# About 1.54 GB used to this point.

"""
Now we need a mapping from (citing, cited) -> (i, j),
complicated by the fact that (i, j) is for uniques.
    Plan: i = (map_citing[map_citing == citing]).index
          j = (map_cited[map_cited == cited]).index
        sp[i, j] = 1
"""
# 4.49 s for first 100, no appreciable memory usage.
# Started at 10:18
# This should be parallizabl. Only using one core really.
# Finished about 
for i in net.index:
    r = net.ix[i]
    sp[(map_citing[map_citing == r['citing']]).index,
        (map_cited[map_cited == r['cited']]).index] = 1

######################### Break Here ##############################
d = {22: 'Computer Hardware & Software',
    24: 'Information Storage',
    25: 'Electronic business methods and software'}

qcat = ut['subcat']
tech = ut[(cat == 22.0) | (cat == 24.0) | (cat == 25.0)]
patents = tech['patent'].unique()

u = np.union1d(net['citing'].unique(), patents)  # 261445 items
# test = net['citing'].apply(lambda x: x in u)
test = u[:100]
gr = test.groupby('cited')
t = gr['citing']
d = {k: v.values for k, v in t}

########
a = net['citing'].unique()
b = net['cited'].unique()
ind = np.union1d(a, b)
idx = pd.Series(ind)


N = np.arange(max_ - min_ - 1)

t_net = net.head(10000)

t_a = t_net['citing'].unique()
t_b = t_net['cited'].unique()
t_ind = np.union1d(t_a, t_b)
t_idx = pd.Series(t_ind)

rows = []
cols = []

for k in t_net.index:
    i = (t_idx[t_idx == t_net.ix[k]['citing']]).index[0]
    j = (t_idx[t_idx == t_net.ix[k]['cited']]).index[0]
    rows.append(i)
    cols.append(j)

rows = np.array(rows)
cols = np.array(cols)
data = np.ones(len(t_net))
N = np.max([cols.max(), rows.max()])
sp = sparse.coo_matrix((data, (rows, cols)), shape=(N + 1, N + 1))
