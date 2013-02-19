import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from networkx import graphviz_layout
from scipy import sparse

s = pd.HDFStore('/Volumes/HDD/Users/tom/DataStorage/Patents/patents.h5')
# ut = s['utility']
net = s['cites']

######################### Break Here ##############################
# d = {22: 'Computer Hardware & Software',
#     24: 'Information Storage',
#     25: 'Electronic business methods and software'}
########
####### Full Run ###########

# Only got about .6% there after 2 hours.
a = net['citing'].unique()
b = net['cited'].unique()
ind = np.union1d(a, b)
idx = pd.Series(ind)

rows = []
cols = []

for k in net.index:
    i = (idx[idx == net.ix[k]['citing']]).index[0]
    j = (idx[idx == net.ix[k]['cited']]).index[0]
    rows.append(i)
    cols.append(j)

rows = np.array(rows)
cols = np.array(cols)
data = np.ones(len(net))
N = np.max([cols.max(), rows.max()])
sp = sparse.coo_matrix((data, (rows, cols)), shape=(N + 1, N + 1))

### Practice ###
# t_net = net.head(100)

# t_a = t_net['citing'].unique()
# t_b = t_net['cited'].unique()
# t_ind = np.union1d(t_a, t_b)
# t_idx = pd.Series(t_ind)

# # rows = []
# # cols = []

# # def app(x, rows, cols):
# #     i = (t_idx[t_idx == x['citing']]).index[0]
# #     j = (t_idx[t_idx == x['cited']]).index[0]
# #     rows.append(i)
# #     cols.append(j)

# # t_net.apply(app, axis=1, args=(rows, cols))

# rows = []
# cols = []

# for k in t_net.index:
#     i = (t_idx[t_idx == t_net.ix[k]['citing']]).index[0]
#     j = (t_idx[t_idx == t_net.ix[k]['cited']]).index[0]
#     rows.append(i)
#     cols.append(j)

# rows = np.array(rows)
# cols = np.array(cols)
# data = np.ones(len(t_net))
# N = np.max([cols.max(), rows.max()])
# sp = sparse.coo_matrix((data, (rows, cols)), shape=(N + 1, N + 1))
