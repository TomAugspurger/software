from __future__ import division

import matplotlib

# matplotlib.use("AGG")
"""
Files available from:
https://sites.google.com/site/patentdataproject/Home/downloads

Directly:
http://www.nber.org/~jbessen/patassg.dat.zip
http://www.nber.org/~jbessen/pat76_06_assgasc.zip
"""

import pandas as pd
import matplotlib.pyplot as plt
from patent_lookup import Lookup
# Change path to local version.
s = pd.HDFStore('/Volumes/HDD/Users/tom/DataStorage/Patents/patents.h5')

"""
Just tech industries (see classifications.py)
{46: 'Semiconductor Devices', 21: 'Communications',
   22: 'Computer Hardware & Software',
   23: 'Computer Peripherials', 24: 'Information Storage',
   25: 'Electronic business methods and software']
Some companies of note:
{'amazon': 737570,
'apple' : 32940,
'apple2': 799370,
'google': 706518,
'att': 706518,
'microsoft' : 373780,
'ibm': 280070
}
"""
df = s['utility']
# df = df[df.duplicated('patent')]  # Drop the dupes for multiple assignees.


# def gen_companies(d):
#     """
#     d is a dict of compaines.
#     returns heirarchical dataframe.
#     """
#     d2 = {comp: df[df['uspto_assignee'] == d[comp]] for comp in d}
#     return pd.Panel(d2)
d = {'amazon': 737570,
        'apple': 32940,
        'apple2': 799370,
        'google': 706518,
        'att': 706518,
        'microsoft': 373780,
        'ibm': 280070}
inv_d = {d[k]: k for k in d}
# wp = gen_companies(d)

sub = df[df['uspto_assignee'].isin(d.values())]
gr = sub.groupby(['uspto_assignee', 'appyear'])
cts = gr['patent'].count().unstack(level='uspto_assignee')
cts = cts.rename(columns=inv_d)
ax = cts.plot()
plt.savefig('../resources/by_company.png')
