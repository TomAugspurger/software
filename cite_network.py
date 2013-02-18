"""
Based on the citations datafile:

http://elsa.berkeley.edu/~bhhall/pat/cite76_06.zip

Note tested for now on the 75-99 file.  The full is STATA only
and I need to get a campus computer to read it and convert to a csv.
Might add new dependencies: networkgraphx and pygraphviz
the latter depends on graphviz (which is installed via brew)

"""

import pandas as pd
import pygraphviz as pgv

df = pd.read_csv('cite75_99.txt')
gr = df.groupby('CITING')  # Careful when working with this guy.

u = df['CITING'].unique()
test = u[:100]
d = {c: df['CITED'][df['CITING'] == c].values for c in test}

A = pgv.AGraph(d, directed=True)
A.layout(prog='neato')  # Set graph structure. Don't use fdp.
A.draw('test_neato.png')
