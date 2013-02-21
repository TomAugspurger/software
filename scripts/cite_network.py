"""
Based on the citations datafile:

http://elsa.berkeley.edu/~bhhall/pat/cite76_06.zip

Cleaning:
import pandas as pd
import statsmodels.api as sm

f = open('cite_76_06.dta')
g = sm.iolib.StataReader(f)
l = [x for x in g.dataset()]  # Took ~ 4.1 GB of ram

df = pd.DataFrame(l)
df.colums = ['citing', 'cited', 'num']
"""

import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from networkx import graphviz_layout

s = pd.HDFStore('/Volumes/HDD/Users/tom/DataStorage/Patents/patents.h5')
df = s['cites']
gr = df.groupby('citing')  # Careful when working with this guy.

test = df[:100]

# Method 1
# d = {c: df['cited'][df['citing'] == c].values for c in test}


# Method 2
gr = test.groupby('cited')
t = gr['citing']
d = {k: v.values for k, v in t}


A = nx.Graph(d, directed=True)
pos = nx.graphviz_layout(A, prog='twopi', root=0)
nx.draw(A, pos, with_labels=False, alpha=.5)
plt.draw()
fig = plt.gcf()
ax = fig.axes[0]
plt.savefig('test_twopi.png')
